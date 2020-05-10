
import sqlite3


class Database():
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self, db_file='fashion.db'):
        # create database connection
        return sqlite3.connect(db_file)

    def select_products(self):
        sql = "SELECT * FROM products;"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
