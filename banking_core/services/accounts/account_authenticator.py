from banking_core.services import PinHasher

class AccountAuthenticator:
    def __init__(self, db, pin_hasher, account_locker):
        self.db = db
        self.pin_hasher = pin_hasher
        self.account_locker = account_locker

    def log_into_account(self, account_id, pin):
        result = self.db.fetch_one("SELECT id, pin, failed_attempts, locked FROM account WHERE id = %s",
                                   (card_number,))

        if result:
            stored_account_id, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("Your account is already locked.")

            if PinHasher.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE account SET failed_attempts = 0 WHERE number = %s", (account_id,))
                return True
            else:
                self.account_locker.lock_account_after_failed_attempt(account_id)
                return False
        else:
            raise ValueError("Account not found.")