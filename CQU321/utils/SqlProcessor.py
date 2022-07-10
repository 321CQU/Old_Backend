import json
import traceback
from datetime import datetime

import pymysql
from configparser import ConfigParser

from Website.settings import BASE_DIR

db_config = ConfigParser()
db_config.read(str(BASE_DIR) + '/CQU321/321CQU_Config.ini')


def _connect_db():
    connection = pymysql.connect(
        host=db_config.get('321CQU_Database', 'host'),
        port=db_config.getint('321CQU_Database', 'port'),
        user=db_config.get('321CQU_Database', 'user'),
        password=db_config.get('321CQU_Database', 'password'),
        database=db_config.get('321CQU_Database', 'database')
    )
    cursor = connection.cursor()
    return connection, cursor


class SqlProcessor:
    def __init__(self):
        connection, cursor = _connect_db()
        self.connection = connection
        self.cursor = cursor

    def execute(self, query, args=None):
        try:
            self.cursor.execute(query, args)
        except Exception as e:
            params = {
                'query': query,
                'args': json.dumps(args)
            }
            with open(str(BASE_DIR) + '/exception_infos/' + 'sql_exception.txt', 'a') as f:
                f.write(datetime.now().strftime('"%Y-%m-%d %H:%M:%S"') + '\n')
                f.write('params:\n' + json.dumps(params) + '\n')
                f.write(traceback.format_exc())

            self.connection.rollback()
            return False
        else:
            self.connection.commit()
            return True

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchmany(self, size):
        return self.cursor.fetchmany(size)

