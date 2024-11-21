from banking_core.services import PinHasher
from banking_core.database import DailyLimitManager
from datetime import datetime

class LimitManager:
    def __init__(self, db):
        self.db = db
        self.daily_limit_manager = DailyLimitManager(db)

    def set_daily_limit(self, card_number):
        try:
            limit_data = self.db.get_daily_limit(card_number)

            if limit_data:
                daily_limit, changes_today, set_date = limit_data
                print(f"Daily limit: {daily_limit}, Changes today: {changes_today}, Set date: {set_date}")

                if set_date == str(datetime.now().date()) and changes_today >= 3:
                    print("You have reached the maximum number of changes for today. Try again tomorrow.")
                    return
            else:
                print("No daily limit set for this account.")

            pin = input("Enter your PIN to confirm: ")
            stored_pin = self.get_stored_pin(card_number)

            if not PinHasher.check_pin(stored_pin, pin):
                print("Invalid PIN.")
                return

            new_limit = self.get_new_limit()

            self.update_or_add_limit(card_number, new_limit, limit_data)
            print(f"Your daily limit has been set to {new_limit}.")

        except Exception as e:
            print(f"An error occurred while setting the daily limit: {e}")

    def get_stored_pin(self, card_number):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT pin FROM card WHERE number = %s", (card_number,))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Card number not found.")
        return result[0]

    def get_new_limit(self):
        while True:
            try:
                new_limit = int(input("Enter your new daily transaction limit: "))
                if new_limit <= 0:
                    raise ValueError("Daily limit must be greater than zero.")
                return new_limit
            except ValueError as ve:
                print(f"Invalid input: {ve}. Please try again.")

    def update_or_add_limit(self, card_number, new_limit, limit_data):
        current_date = str(datetime.now().date())
        if limit_data:
            self.db.update_daily_limit(card_number, new_limit)
        else:
            self.db.add_daily_limit(card_number, new_limit)