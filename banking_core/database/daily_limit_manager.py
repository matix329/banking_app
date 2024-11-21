from datetime import datetime
from banking_core.database.base_manager import BaseManager

class DailyLimitManager:
    def __init__(self, db):
        self.db = db

    def get_daily_limit(self, account_number):
        return self.db.fetch_one('''SELECT daily_limit, changes_today, set_date 
                                    FROM daily_limits WHERE account_number = %s ORDER BY set_date DESC LIMIT 1''', (account_number,))

    def add_daily_limit(self, account_number, daily_limit):
        current_date = datetime.now().date()
        self.db.execute_query('''INSERT INTO daily_limits (account_number, daily_limit, set_date, changes_today)
                                 VALUES (%s, %s, %s, %s)''', (account_number, daily_limit, str(current_date), 0))

    def update_daily_limit(self, account_number, new_limit):
        current_date = datetime.now().date()
        self.db.execute_query('''UPDATE daily_limits
                                 SET daily_limit = %s, set_date = %s, changes_today = changes_today + 1
                                 WHERE account_number = %s AND set_date = %s''', (new_limit, str(current_date), account_number, str(current_date)))