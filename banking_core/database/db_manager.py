import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="card.s3db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.setup_database()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise Exception(f"Database connection error: {e}")

    def setup_database(self):
        if self.conn:
            try:
                with self.conn:
                    self.conn.execute('''CREATE TABLE IF NOT EXISTS card (
                                            id INTEGER PRIMARY KEY,
                                            number TEXT UNIQUE,
                                            pin TEXT,
                                            balance INTEGER DEFAULT 0,
                                            failed_attempts INTEGER DEFAULT 0,
                                            locked BOOLEAN DEFAULT 0
                                        );''')
                    self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            account_number TEXT,
                                            transaction_type TEXT,
                                            amount INTEGER,
                                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            FOREIGN KEY (account_number) REFERENCES card(number)
                                        );''')
                    self.conn.execute('''CREATE TABLE IF NOT EXISTS daily_limits (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            account_number TEXT,
                                            daily_limit INTEGER,
                                            set_date TEXT,
                                            changes_today INTEGER DEFAULT 0,
                                            FOREIGN KEY (account_number) REFERENCES card(number)
                                        );''')
            except sqlite3.Error as e:
                print(f"Error setting up the database: {e}")
                raise
        else:
            print("Error: Database connection is not available")
            raise Exception("Database connection is not available")

    def execute_query(self, query, params=()):
        if self.conn:
            try:
                with self.conn:
                    self.conn.execute(query, params)
            except sqlite3.Error as e:
                print(f"Database query error: {e}")
                raise
        else:
            print("Error: Database connection is not available")
            raise Exception("Database connection is not available")

    def fetch_one(self, query, params=()):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            except sqlite3.Error as e:
                print(f"Database query error: {e}")
                raise
        else:
            print("Error: Database connection is not available")
            raise Exception("Database connection is not available")

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error as e:
                print(f"Error closing the database connection: {e}")
                raise
        else:
            print("Error: No database connection to close")
            raise Exception("No database connection to close.")

    def get_daily_limit(self, account_number):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT daily_limit, changes_today, set_date 
                          FROM daily_limits WHERE account_number = ? ORDER BY set_date DESC LIMIT 1''',
                       (account_number,))
        result = cursor.fetchone()
        if result:
            return result
        return None

    def add_daily_limit(self, account_number, daily_limit):
        cursor = self.conn.cursor()
        current_date = datetime.now().date()
        try:
            cursor.execute('''INSERT INTO daily_limits (account_number, daily_limit, set_date, changes_today)
                              VALUES (?, ?, ?, ?)''', (account_number, daily_limit, str(current_date), 0))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding daily limit: {e}")
            raise

    def update_daily_limit(self, account_number, new_limit):
        cursor = self.conn.cursor()
        current_date = datetime.now().date()
        try:
            cursor.execute('''UPDATE daily_limits
                              SET daily_limit = ?, set_date = ?, changes_today = changes_today + 1
                              WHERE account_number = ? AND set_date = ?''',
                           (new_limit, str(current_date), account_number, str(current_date)))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating daily limit: {e}")
            raise