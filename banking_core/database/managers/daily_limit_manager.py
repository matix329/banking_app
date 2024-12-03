from datetime import datetime

class DailyLimitManager:
    def __init__(self, db):
        self.db = db

    def get_daily_limit(self, sub_account_id):
        return self.db.fetch_one('''SELECT daily_limit, changes_today, set_date 
                                    FROM daily_limits WHERE sub_account_id = %s ORDER BY set_date DESC LIMIT 1''', (sub_account_id,))

    def add_daily_limit(self, sub_account_id, daily_limit):
        current_date = datetime.now().date()
        self.db.execute_query('''INSERT INTO daily_limits (sub_account_id, daily_limit, set_date, changes_today)
                                 VALUES (%s, %s, %s, %s)''', (sub_account_id, daily_limit, str(current_date), 0))

    def update_daily_limit(self, sub_account_id, new_limit):
        current_date = datetime.now().date()
        self.db.execute_query('''UPDATE daily_limits
                                 SET daily_limit = %s, set_date = %s, changes_today = changes_today + 1
                                 WHERE sub_account_id = %s AND set_date = %s''', (new_limit, str(current_date), sub_account_id, str(current_date)))