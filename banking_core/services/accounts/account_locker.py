from banking_core.services import PinHasher

class AccountLocker:
    def __init__(self, db):
        """
        Initializes the AccountLocker with the provided database instance.

        Parameters
        ----------
        db : object
            The database instance to execute queries on.
        """
        self.db = db

    def get_account_status(self, card_number):
        result = self.db.fetch_one("SELECT failed_attempts, locked FROM card WHERE number = %s", (card_number,))
        if not result:
            raise ValueError("Account not found.")
        failed_attempts, locked = result
        return failed_attempts, locked

    def lock_account(self, card_number, pin):
        result = self.db.fetch_one("SELECT number, pin, failed_attempts, locked FROM card WHERE number = %s",
                                   (card_number,))

        if result:
            stored_card_number, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("Your account is already locked.")

            if PinHasher.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE card SET locked = TRUE, failed_attempts = 0 WHERE number = %s",
                                      (card_number,))
                return True
            else:
                raise ValueError("Incorrect PIN. Please try again.")
        else:
            raise ValueError("Account with specified card number not found. Please double-check the number.")

    def unlock_account(self, card_number):
        _, locked = self.get_account_status(card_number)
        if not locked:
            raise ValueError("This account is not locked.")
        self.db.execute_query("UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = %s", (card_number,))

    def lock_account_after_failed_attempt(self, card_number):
        failed_attempts, locked = self.get_account_status(card_number)
        if locked:
            raise ValueError("Your account is already locked.")
        failed_attempts += 1
        self.db.execute_query("UPDATE card SET failed_attempts = %s WHERE number = %s", (failed_attempts, card_number))
        if failed_attempts >= 3:
            self.lock_account(card_number)
            raise ValueError("Your account has been locked due to multiple failed login attempts.")