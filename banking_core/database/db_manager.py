import sqlite3

class DatabaseManager:
    def __init__(self, db_name="card.s3db"):
        self.conn = sqlite3.connect(db_name)
        self.setup_database()

    def setup_database(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS card (
                                    id INTEGER PRIMARY KEY,
                                    number TEXT UNIQUE,
                                    pin TEXT,
                                    balance INTEGER DEFAULT 0
                                );''')

    def execute_query(self, query, params=()):
        with self.conn:
            self.conn.execute(query, params)

    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        self.conn.close()
