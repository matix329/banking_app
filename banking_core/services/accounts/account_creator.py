import random
from ..utils.constants import CARD_PREFIX, CARD_LENGTH, PIN_LENGTH
from banking_core.services import PinHasher

class AccountCreator:
    """
    A class used to create new bank accounts.

    ...

    Attributes
    ----------
    db : object
        the database instance used for storing and retrieving account data

    Methods
    -------
    create_account()
        Creates a new account with a unique card number and a secure PIN.
    generate_card_number()
        Generates a valid card number following the Luhn algorithm.
    generate_pin()
        Creates a random numeric PIN of a predefined length.
    calculate_luhn_checksum(partial_card_number)
        Calculates the Luhn checksum for a partial card number.
    """
    def __init__(self, db):
        """
        Initializes the AccountCreator with the provided database instance.

        Parameters
        ----------
        db : object
        The database instance to execute queries on.
        """
        self.db = db

    def create_account(self):
        """
        Creates a new account by generating a unique card number and a secure PIN.

        The method:
        - Ensures the generated card number is unique in the database.
        - Generates a random PIN for the account.
        - Hashes the PIN for secure storage.
        - Inserts the new account into the database with an initial balance of 0.

        Returns
        -------
        tuple
            A tuple containing the generated card number (str) and the plaintext PIN (str).
        """
        while True:
            card_number = self.generate_card_number()
            if not self.db.fetch_one("SELECT number FROM card WHERE number = %s", (card_number,)):
                break

        pin = self.generate_pin()
        hashed_pin = PinHasher.hash_pin(pin)

        self.db.execute_query("INSERT INTO card (number, pin, balance) VALUES (%s, %s, 0)", (card_number, hashed_pin))
        return card_number, pin

    def generate_card_number(self):
        """
        Generates a valid card number using a prefix, random digits, and a Luhn checksum.

        The card number consists of:
        - A predefined prefix (`CARD_PREFIX`).
        - Randomly generated account digits.
        - A checksum digit calculated using the Luhn algorithm.

        Returns
        -------
        str
            The complete card number.
        """
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(CARD_LENGTH - len(CARD_PREFIX) - 1)])
        partial_card_number = CARD_PREFIX + account_number
        checksum = self.calculate_luhn_checksum(partial_card_number)
        return partial_card_number + str(checksum)

    def generate_pin(self):
        """
        Generates a random numeric PIN.

        The length of the PIN is defined by the constant `PIN_LENGTH`.

        Returns
        -------
        str
            The generated PIN as a numeric string.
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(PIN_LENGTH)])

    def calculate_luhn_checksum(self, partial_card_number):
        """
        Calculates the Luhn checksum for a given partial card number.

        The checksum ensures that the card number complies with the Luhn algorithm.

        Parameters
        ----------
        partial_card_number : str
            The card number without the checksum digit.

        Returns
        -------
        int
            The calculated checksum digit.
        """
        digits = [int(d) for d in partial_card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d * 2))
        return (10 - (checksum % 10)) % 10