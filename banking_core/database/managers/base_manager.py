import psycopg2

class BaseManager:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query, params=()):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                result = None
                if query.strip().upper().startswith("INSERT") and "RETURNING" in query.upper():
                    result = cursor.fetchone()
                self.connection.commit()
                cursor.close()
                return result
            except psycopg2.Error as e:
                print(f"Database query error: {e}")
                self.connection.rollback()
                raise

    def fetch_one(self, query, params=()):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
            except psycopg2.IntegrityError as e:
                raise ValueError(f"Integrity error (e.g., foreign key violation): {e}, Query: {query}, Params: {params}") from e
            except psycopg2.Error as e:
                raise ValueError(f"Database query error: {e}, Query: {query}, Params: {params}") from e
            finally:
                cursor.close()

    def get_daily_limit(self, sub_account_id):
        query = """
            SELECT daily_limit, changes_today, set_date 
            FROM daily_limits 
            WHERE sub_account_id = %s 
            AND set_date::date = CURRENT_DATE
        """
        return self.fetch_one(query, (sub_account_id,))