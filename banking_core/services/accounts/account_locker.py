class AccountLocker:
    def __init__(self, db):
        self.db = db

    def lock_account_after_failed_attempt(self, card_number):
        self.db.execute_query("UPDATE card SET failed_attempts = failed_attempts + 1 WHERE number = %s", (card_number,))
        result = self.db.fetch_one("SELECT failed_attempts, locked FROM card WHERE number = %s", (card_number,))

        if not result:
            raise ValueError("Account not found.")

        failed_attempts = result[0]
        locked = result[1]

        if locked:
            raise ValueError("Your account is already locked.")

        if failed_attempts >= 3:
            self.db.execute_query("UPDATE card SET locked = TRUE WHERE number = %s", (card_number,))
            raise ValueError("Your account has been locked due to multiple failed login attempts.")

    def unlock_account(self, card_number):
        result = self.db.fetch_one("SELECT locked FROM card WHERE number = %s", (card_number,))

        if not result:
            raise ValueError("Account not found.")

        locked = result[0]

        if not locked:
            raise ValueError("This account is not locked.")

        self.db.execute_query("UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = %s", (card_number,))
        print("The account has been unlocked.")