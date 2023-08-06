#!/usr/bin/env python3

from pg_connection import PgConnection
from date_partition_util import DatePartitionUtil
import logging
import argparse
from datetime import datetime
from dateutil import relativedelta

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# returns columns part of a primary key
def TBL_PKEY_SQL(tbl):
    sql = f"""
        select kc.column_name, kc.constraint_name
        from information_schema.table_constraints tc
        join information_schema.key_column_usage kc
            on kc.table_name = tc.table_name and
            kc.table_schema = tc.table_schema and
            kc.constraint_name = tc.constraint_name
        where tc.constraint_type = 'PRIMARY KEY'
        and kc.ordinal_position is not null
        and tc.table_name = '{tbl}'
        order by kc.ordinal_position;
        """
    return sql


# returns sequence (default value) of a column
def TBL_SEQNAME(tbl, col):
    sql = f"""
        select substring(column_default from '''(.+)'''), column_default
        from information_schema.columns
        where (table_schema, table_name) = ('public', '{tbl}')
            and column_name = '{col}';
    """
    return sql


# migrate to partition with logic to add column to primary key
def TBL_CONVERT_FK_SQL(tbl, pkey, seq, cols, pcol):
    new_pkey_cols = list(cols)
    new_pkey_cols.append(pcol)
    sql = f"""
        -- converting primary key
        alter table {tbl} drop constraint {pkey};
        alter table {tbl} add constraint {pkey}
            primary key ({','.join(new_pkey_cols)});
    """
    return sql


def TBL_MIGRATE_SEQ_SQL(tbl, seq, cols):
    return f"""
        -- move sequence ownership to new table
        alter sequence if exists {seq} owned by {tbl}.{cols[0]};
    """


def TBL_MIGRATE_DATA_SQL(tbl):
    sql = f"""
        -- migrate data
        insert into {tbl}
        select * from __old_{tbl};
    """
    return sql


def TBL_DROP_OLDTBL_SQL(tbl):
    return f"""
        -- drop table
        drop table __old_{tbl};
    """


# simple migration to partition table
def TBL_PARTITION_SQL(tbl, pcol):
    sql = f"""
        -- rename table and create replacement
        alter table {tbl} rename to __old_{tbl};
        create table {tbl} (like __old_{tbl} including all)
            partition by range({pcol});
    """
    return sql


class PgPartiton(object):
    def __init__(self):
        self.pgconn = PgConnection()
        self.pgconn.connect()
        self.pu = DatePartitionUtil()

    def is_connected(self):
        return self.pgconn.connected

    def execute(self, sql):
        self.pgconn.execute(sql)

    def partition_by_day(self, tbl, d):
        dp = self.pu.day_partition(d)
        return self.pu.make_partition_query(tbl, dp)

    def partition_by_week(self, tbl, d):
        dp = self.pu.week_partition(d)
        return self.pu.make_partition_query(tbl, dp)

    def partition_by_month(self, tbl, d):
        dp = self.pu.month_partition(d)
        return self.pu.make_partition_query(tbl, dp)

    def table_date_range(self, tbl, column):
        d = self.pgconn.execute_fetch_one(
            f'select min({column}), max({column}) from {tbl}')
        if d:
            return (d[0], d[1])
        return None

    def partition_table(self, table, column, ptype=None):
        # 0. check i f table has data and force migration partition type
        ranges = self.table_date_range(table, column)
        if ranges and ranges != (None, None):
            if not ptype:
                log.error(f'Table {table} has data. Specify partition type {ranges}')
                exit(-1)
            # migrate data
            log.info(f'min: {ranges[0]}, max: {ranges[1]}, type: {ptype}')

        # 1. partition key should ref unique constraints
        data = self.pgconn.execute_fetch_all(TBL_PKEY_SQL(table))
        pcols = [i[0] for i in data]
        seq = None
        if pcols:
            seq = self.pgconn.execute_fetch_one(TBL_SEQNAME(table, pcols[0]))
        q = ""
        if data and column not in pcols:
            # partition column is not part of primary key, replace and add
            log.info(f'Col {column} is not part of pkey {data}')
            pkey = [i[1] for i in data]
            if seq and pkey:
                # migrate foreign key
                q += TBL_CONVERT_FK_SQL(table, pkey[0], seq[0], pcols, column)
        # migrate partition
        q += TBL_PARTITION_SQL(table, column)
        # migrate sequence
        if seq:
            q += TBL_MIGRATE_SEQ_SQL(table, seq[0], pcols)
        # prepare partitions for data
        if ptype and ranges:
            i = 0
            tpl = pfunc[ptype]
            start = ranges[0]
            while(True):
                d = start + relativedelta.relativedelta(**{tpl[1]: i})
                q += "\t" + tpl[0](args.table, d) + "\n"
                i += 1
                if d > ranges[1]:
                    break
            # do actual migration
            q += TBL_MIGRATE_DATA_SQL(table)
        # drop old table
        q += TBL_DROP_OLDTBL_SQL(table)

        log.info(q)
        self.pgconn.execute(q)


if __name__ == "__main__":
    pgpart = PgPartiton()
    pfunc = {
        'day': (pgpart.partition_by_day, 'days'),
        'week': (pgpart.partition_by_week, 'weeks'),
        'month': (pgpart.partition_by_month, 'months')
    }
    if pgpart.is_connected():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        # parser for creating the table partition
        cp = subparsers.add_parser('create')
        cp.add_argument("table", help="table to be partitioned", type=str)
        cp.add_argument("column", help="column to be used for range", type=str)
        cp.add_argument("--type",
                        choices=['day', 'week', 'month'], type=str)
        # parser to add the partions
        ap = subparsers.add_parser('add')
        ap.add_argument("table", help="table to be partitioned", type=str)
        ap.add_argument("type",
                        choices=['day', 'week', 'month'], type=str)
        ap.add_argument("--num", help="partitions to create",
                        type=int, default=1)
        ap.add_argument("--date", help="start date (yyyymmdd)", type=str)

        args = parser.parse_args()
        if 'column' in args:
            print(f'Create partition {args.table} with col {args.column}')
            pgpart.partition_table(args.table, args.column, args.type)
        else:
            start = datetime.today()
            if args.date:
                start = datetime.strptime(args.date, '%Y%m%d')
            print(f'Add {args.num} {args.type} partition(s) to {args.table}')
            for i in range(args.num):
                tpl = pfunc[args.type]
                d = start + relativedelta.relativedelta(**{tpl[1]: i})
                q = tpl[0](args.table, d)
                log.info(q)
                pgpart.execute(q)
    else:
        log.error('Not connected to db')
