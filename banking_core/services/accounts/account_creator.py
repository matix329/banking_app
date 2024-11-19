import random
from banking_core.utils.constants import CARD_PREFIX, CARD_LENGTH, PIN_LENGTH
from banking_core.services.utils.pin_hasher import PinHasher

class AccountCreator:
    def __init__(self, db):
        self.db = db

    def create_account(self):
        while True:
            card_number = self.generate_card_number()
            if not self.db.fetch_one("SELECT number FROM card WHERE number = %s", (card_number,)):
                break

        pin = self.generate_pin()
        hashed_pin = PinHasher.hash_pin(pin)

        self.db.execute_query("INSERT INTO card (number, pin, balance) VALUES (%s, %s, 0)", (card_number, hashed_pin))
        return card_number, pin

    def generate_card_number(self):
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(CARD_LENGTH - len(CARD_PREFIX) - 1)])
        partial_card_number = CARD_PREFIX + account_number
        checksum = self.calculate_luhn_checksum(partial_card_number)
        return partial_card_number + str(checksum)

    def generate_pin(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(PIN_LENGTH)])

    def calculate_luhn_checksum(self, partial_card_number):
        digits = [int(d) for d in partial_card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d * 2))
        return (10 - (checksum % 10)) % 10