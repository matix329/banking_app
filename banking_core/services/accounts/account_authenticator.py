from banking_core.services import PinHasher

class AccountAuthenticator:
    def __init__(self, db, pin_hasher, account_locker):
        self.db = db
        self.pin_hasher = pin_hasher
        self.account_locker = account_locker

    def log_into_account(self, card_number, pin):
        result = self.db.fetch_one("SELECT number, pin, failed_attempts, locked FROM card WHERE number = %s",
                                   (card_number,))

        if result:
            stored_card_number, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("This account is locked due to multiple failed login attempts.")

            if self.pin_hasher.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE card SET failed_attempts = 0 WHERE number = %s", (card_number,))
                return True
            else:
                self.account_locker.lock_account_after_failed_attempt(card_number)
                return False
        return False