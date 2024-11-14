import sqlite3

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
                                            balance INTEGER DEFAULT 0
                                        );''')
                    self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            account_number TEXT,
                                            transaction_type TEXT,
                                            amount INTEGER,
                                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                            FOREIGN KEY (account_number) REFERENCES card(number)
                                        )''')
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