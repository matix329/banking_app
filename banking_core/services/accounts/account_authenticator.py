from banking_core.services import PinHasher

class AccountAuthenticator:
    """
    A class used to authenticate users attempting to log into their accounts.

    ...

    Attributes
    ----------
    db : object
        The database instance used for querying account data.
    pin_hasher : object
        The instance used for securely hashing and verifying PIN codes.
    account_locker : object
        The instance responsible for handling account locking after failed login attempts.

    Methods
    -------
    log_into_account(card_number, pin)
        Authenticates the user by verifying the provided card number and PIN.
    """
    def __init__(self, db, pin_hasher, account_locker):
        """
        Initializes the AccountAuthenticator with the provided dependencies.

        Parameters
        ----------
        db : object
            The database instance to execute queries on.
        pin_hasher : object
            The instance used for securely hashing and checking PIN codes.
        account_locker : object
            The instance responsible for locking accounts after failed attempts.
        """
        self.db = db
        self.pin_hasher = pin_hasher
        self.account_locker = account_locker

    def log_into_account(self, card_number, pin):
        """
        Authenticates a user by verifying their card number and PIN.

        The method performs the following steps:
        - Fetches account details (card number, hashed PIN, failed attempts, and lock status) from the database.
        - Checks if the account is locked. If so, raises an exception.
        - Verifies the provided PIN against the hashed PIN stored in the database.
        - If the PIN is correct, resets the failed attempts counter and allows login.
        - If the PIN is incorrect, increments the failed attempts counter and locks the account if necessary.

        Parameters
        ----------
        card_number : str
            The card number of the account to log into.
        pin : str
            The plaintext PIN provided by the user for authentication.

        Returns
        -------
        bool
            `True` if authentication is successful (PIN is correct).
            `False` if authentication fails (PIN is incorrect).

        Raises
        ------
        ValueError
            If the account is not found or is already locked.
        """
        result = self.db.fetch_one("SELECT number, pin, failed_attempts, locked FROM card WHERE number = %s",
                                   (card_number,))

        if result:
            stored_card_number, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("Your account is already locked.")

            if PinHasher.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE card SET failed_attempts = 0 WHERE number = %s", (card_number,))
                return True
            else:
                self.account_locker.lock_account_after_failed_attempt(card_number)
                return False
        else:
            raise ValueError("Account not found.")