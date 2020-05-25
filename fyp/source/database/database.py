
import sqlite3


class Database():
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self, db_file='database/fashion.db'):
        # create database connection
        return sqlite3.connect(db_file)

    def select_user_products(self, user_id=''):
        sql = "SELECT users.id AS user, rating, products.id As product, products.* FROM users\
            INNER JOIN rating on rating.user_id = users.id\
            INNER JOIN products on rating.product_id = products.id"
        if user_id:
            sql += " WHERE user.id = '" + user_id + "'"
        else:
            sql += ";"
        return sql

    def select_all(self, table):
        sql = "SELECT * FROM " + table + ";"
        return sql
