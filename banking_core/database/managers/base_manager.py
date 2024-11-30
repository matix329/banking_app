import psycopg2

class BaseManager:
    def __init__(self, connection):
        self.conn = connection

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

    def fetch_one(self, query, params=()):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            except psycopg2.Error as e:
                print(f"Database query error: {e}")
                raise

    def get_daily_limit(self, account_id, currency):
        query = """
            SELECT daily_limit, changes_today, set_date 
            FROM daily_limits 
            WHERE account_id = %s
            AND currency = %s 
            AND set_date::date = CURRENT_DATE
        """
        return self.fetch_one(query, (account_id, currency))