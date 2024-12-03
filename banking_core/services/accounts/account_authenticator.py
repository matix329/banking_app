from ..utils.pin_hasher import PinHasher

class AccountAuthenticator:
    def __init__(self, db, pin_hasher, account_locker):
        self.db = db
        self.pin_hasher = pin_hasher
        self.account_locker = account_locker

    def log_into_account(self, account_number, pin):
        result = self.db.fetch_one("SELECT id, pin, failed_attempts, locked FROM account WHERE account_number = %s",
                                   (account_number,))

        if result:
            stored_account_id, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("Your account is already locked.")

            if self.pin_hasher.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE account SET failed_attempts = 0 WHERE account_number = %s", (account_number,))
                return True
            else:
                self.account_locker.lock_account_after_failed_attempt(account_number)
                return False
        else:
            raise ValueError("Account not found.")