import sqlite3
import os
from utils import logger


class Seta_sqlite:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def update_sql(self, table: str, rec: str, where: str = ''):
        if not where == '':
            where = ' WHERE ' + where
        self.sql("UPDATE " + table + " SET " + rec + where)
        return True

    def insert_sql(self, table: str, rec: str, val: str):
        self.sql("INSERT into " + table + " (" + rec + ") VALUES (" + val + ")")
        return True

    def select_sql(self, table: str, rec: str, rule: str = ''):
        return self.sql("SELECT " + rec + " FROM " + table + ' ' + rule, True)

    def delete_sql(self, table: str, rule: str):
        self.sql("DELETE FROM " + table + " " + rule)

    def is_sql(self, table: str, rule: str = ''):
        result = self.sql("select exists(select * from " + table + ' ' + rule + ")", True)
        return result[0][0]

    def sql(self, qur, rt=False):
        logger.debug(qur)
        self.cur.execute(qur)
        if rt:
            return self.cur.fetchall()
        else:
            self.conn.commit()
