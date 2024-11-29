import psycopg2
import os
from dotenv import load_dotenv

class DatabaseConnection:
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
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            raise Exception(f"Database connection error: {e}")

    def get_connection(self):
        return self.conn

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except psycopg2.Error as e:
                print(f"Error closing the database connection: {e}")
                raise