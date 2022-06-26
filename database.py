import sqlite3, os

class Database:
    def __init__(self, name: str):
        self.connection = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/' + name + '.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def query(self, sql: str, params = ()):
        self.cursor.execute(sql, params)
        self.connection.commit()

    def query_ex(self, sql: str, params = ()):
        return self.cursor.execute(sql, params).fetchall()