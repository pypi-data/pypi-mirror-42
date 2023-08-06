import psycopg2
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class PgConnection(object):
    def __init__(self):
        self.conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    @property
    def connected(self):
        if self.conn and self.execute_fetch_one('SELECT 1'):
            return True
        return False

    def connect(self):
        try:
            dbparam = {
                'host': environ.get('DATABASE_HOST', 'database'),
                'dbname': environ.get('DATABASE_NAME', 'externaldata'),
                'user': environ.get('DATABASE_USER', 'externaldata'),
                'password': environ.get('DATABASE_PASSWORD', 'insecure')
            }
            self.conn = psycopg2.connect(**dbparam)
        except Exception as e:
            log.error(e)
            log.error("Database connection Failed!")
            log.error(dbparam)

    def execute(self, sql):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                self.conn.commit()
        except Exception as e:
            log.error(e)
            self.conn.rollback()

    def execute_fetch_one(self, sql):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchone()
        except Exception as e:
            log.error(e)
            self.conn.rollback()
            return None

    def execute_fetch_all(self, sql):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        except Exception as e:
            log.error(e)
            self.conn.rollback()
            return None
