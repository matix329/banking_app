from banking_core.services import PinHasher

class AccountLocker:
    """
    A class used to handle account locking and unlocking based on login attempts or manual actions.

    ...

    Attributes
    ----------
    db : object
        The database instance used for querying and updating account data.

    Methods
    -------
    get_account_status(card_number)
        Retrieves the status of the account, including failed login attempts and lock status.
    lock_account(card_number, pin)
        Locks the account if the provided PIN is correct and the account is not already locked.
    unlock_account(card_number)
        Unlocks the account if it is currently locked.
    lock_account_after_failed_attempt(card_number)
        Handles the logic for incrementing failed login attempts and locking the account if necessary.
    """
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
        """
        Retrieves the status of the account, including the number of failed attempts and whether the account is locked.

        Parameters
        ----------
        card_number : str
            The card number of the account to check.

        Returns
        -------
        tuple
            A tuple containing:
            - failed_attempts (int): The number of failed login attempts.
            - locked (bool): The lock status of the account.

        Raises
        ------
        ValueError
            If the account is not found.
        """
        result = self.db.fetch_one("SELECT failed_attempts, locked FROM card WHERE number = %s", (card_number,))
        if not result:
            raise ValueError("Account not found.")
        failed_attempts, locked = result
        return failed_attempts, locked

    def lock_account(self, card_number, pin):
        """
        Locks the account if the provided PIN is correct and the account is not already locked.

        Parameters
        ----------
        card_number : str
            The card number of the account to lock.
        pin : str
            The plaintext PIN provided for verification.

        Returns
        -------
        bool
            `True` if the account was successfully locked.

        Raises
        ------
        ValueError
            If the account is already locked, the PIN is incorrect, or the account is not found.
        """
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
        """
        Unlocks the account if it is currently locked.

        Parameters
        ----------
        card_number : str
            The card number of the account to unlock.

        Raises
        ------
        ValueError
            If the account is not locked or is not found.
        """
        _, locked = self.get_account_status(card_number)
        if not locked:
            raise ValueError("This account is not locked.")
        self.db.execute_query("UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = %s", (card_number,))

    def lock_account_after_failed_attempt(self, card_number):
        """
        Handles failed login attempts by incrementing the counter and locking the account if necessary.

        Parameters
        ----------
        card_number : str
            The card number of the account to handle.

        Raises
        ------
        ValueError
            If the account is already locked or if the account is locked due to multiple failed attempts.
        """
        failed_attempts, locked = self.get_account_status(card_number)
        if locked:
            raise ValueError("Your account is already locked.")
        failed_attempts += 1
        self.db.execute_query("UPDATE card SET failed_attempts = %s WHERE number = %s", (failed_attempts, card_number))
        if failed_attempts >= 3:
            self.lock_account(card_number)
            raise ValueError("Your account has been locked due to multiple failed login attempts.")