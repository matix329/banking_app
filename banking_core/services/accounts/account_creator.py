import random
import string
from ..utils.constants import CARD_PREFIX, CARD_LENGTH, PIN_LENGTH
from ..utils.hasher import Hasher

class AccountCreator:
    def __init__(self, db, customer_id):
        self.db = db
        self.customer_id = customer_id

    def create_account(self):
        while True:
            account_number = self.generate_account_number()
            if not self.db.fetch_one("SELECT account_number FROM account WHERE account_number = %s", (account_number,)):
                break

        password = self.generate_password()
        hashed_password = Hasher.hash(password)

        self.db.execute_query(
            "INSERT INTO account (customer_id, account_number, password) VALUES (%s, %s, %s)",
            (self.customer_id, account_number, hashed_password)
        )
        return account_number, password

    def generate_card_number(self):
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(CARD_LENGTH - len(CARD_PREFIX) - 1)])
        partial_card_number = CARD_PREFIX + account_number
        checksum = self.calculate_luhn_checksum(partial_card_number)
        return partial_card_number + str(checksum)

    def generate_pin(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(PIN_LENGTH)])

    def generate_cvv(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])

    def calculate_luhn_checksum(self, partial_card_number):
        digits = [int(d) for d in partial_card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d * 2))
        return (10 - (checksum % 10)) % 10