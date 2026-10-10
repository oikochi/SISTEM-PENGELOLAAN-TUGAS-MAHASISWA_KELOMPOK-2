import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.database = "pengelolaan_tugas"
        self.user = "root"
        self.password = ""
        self.connection = None

    def get_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Koneksi Database Gagal: {e}")
            return None