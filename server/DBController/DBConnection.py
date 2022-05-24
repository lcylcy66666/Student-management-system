import sqlite3
from threading import Lock


class DBConnection:
    db_file_path = str()
    db_lock = Lock()

    def __init__(self):
        DBConnection.db_lock.acquire()
        self.connection = sqlite3.connect(self.db_file_path)
        self.connection.row_factory = sqlite3.Row

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        DBConnection.db_lock.release()
