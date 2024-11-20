import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.setup_database()
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            raise Exception(f"Database connection error: {e}")

    def setup_database(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS card (
                                    id SERIAL PRIMARY KEY,
                                    number TEXT UNIQUE,
                                    pin TEXT,
                                    balance INTEGER DEFAULT 0,
                                    failed_attempts INTEGER DEFAULT 0,
                                    locked BOOLEAN DEFAULT FALSE
                                );''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                    id SERIAL PRIMARY KEY,
                                    account_number TEXT,
                                    transaction_type TEXT,
                                    amount INTEGER,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    FOREIGN KEY (account_number) REFERENCES card(number)
                                );''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS daily_limits (
                                    id SERIAL PRIMARY KEY,
                                    account_number TEXT,
                                    daily_limit INTEGER,
                                    set_date TEXT,
                                    changes_today INTEGER DEFAULT 0,
                                    FOREIGN KEY (account_number) REFERENCES card(number)
                                );''')
                self.conn.commit()
                cursor.close()
            except psycopg2.Error as e:
                print(f"Error setting up the database: {e}")
                raise
        else:
            print("Error: Database connection is not available")
            raise Exception("Database connection is not available")

    def execute_query(self, query, params=()):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query, params)
                self.conn.commit()
                cursor.close()
            except psycopg2.Error as e:
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
            except psycopg2.Error as e:
                print(f"Database query error: {e}")
                raise
        else:
            print("Error: Database connection is not available")
            raise Exception("Database connection is not available")

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except psycopg2.Error as e:
                print(f"Error closing the database connection: {e}")
                raise
        else:
            print("Error: No database connection to close")
            raise Exception("No database connection to close.")

    def get_daily_limit(self, account_number):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT daily_limit, changes_today, set_date 
                          FROM daily_limits WHERE account_number = %s ORDER BY set_date DESC LIMIT 1''',
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
                              VALUES (%s, %s, %s, %s)''', (account_number, daily_limit, str(current_date), 0))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error adding daily limit: {e}")
            raise

    def update_daily_limit(self, account_number, new_limit):
        cursor = self.conn.cursor()
        current_date = datetime.now().date()
        try:
            cursor.execute('''UPDATE daily_limits
                              SET daily_limit = %s, set_date = %s, changes_today = changes_today + 1
                              WHERE account_number = %s AND set_date = %s''',
                           (new_limit, str(current_date), account_number, str(current_date)))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating daily limit: {e}")
            raise

    def lock_account(self, card_number):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE card SET locked = TRUE WHERE number = %s''', (card_number,))
        self.conn.commit()

    def unlock_account(self, card_number):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = %s''', (card_number,))
        self.conn.commit()