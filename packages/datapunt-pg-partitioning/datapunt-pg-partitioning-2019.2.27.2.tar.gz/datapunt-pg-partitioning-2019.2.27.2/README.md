# pg_partition
Utility to partition new/existing PostgreSql database tables. Data can be migrated. Only date range partition type is supported.

Required environment variables:
```
DATABASE_HOST : hostname/ip of the PostgreSql server
DATABASE_NAME : database to operate on
DATABASE_USER : PostgreSql login
DATABASE_PASSWORD : PostgreSql password
```

#### Install ####
```
pip install -r requirements.txt
```

#### Usage ####
```
usage: pg_partition.py [-h] {create,add} ...

positional arguments:
  {create,add}

optional arguments:
  -h, --help    show this help message and exit
```

#### Create Usage ####
```
usage: pg_partition.py create [-h] [--type {day,week,month}] table column

positional arguments:
  table                 table to be partitioned
  column                column to be used for range

optional arguments:
  -h, --help            show this help message and exit
  --type {day,week,month}
```

#### Add Usage ####
```
usage: pg_partition.py add [-h] [--num NUM] [--date DATE]
                           table {day,week,month}

positional arguments:
  table             table to be partitioned
  {day,week,month}

optional arguments:
  -h, --help        show this help message and exit
  --num NUM         partitions to create
  --date DATE       start date (yyyymmdd)
```

#### Creating partitions ####
```
# Convert 'table' to a range partitioned table by 'column'
# No data is migrated
python pg_partition.py create table column

# Convert 'table' to a range partitioned table by 'column'
# Data is migrated in week partitions 
python pg_partition.py create table column --type week
```

#### Adding partitions ####
```
# Adds 10 day partitions starting from 20180101 to 'table'
python pg_partition.py add table day --num 10 --date 20180101

```
