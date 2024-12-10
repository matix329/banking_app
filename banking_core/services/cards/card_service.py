import random
from ..utils.constants import CARD_PREFIX, CARD_LENGTH, PIN_LENGTH

class CardService:

    @staticmethod
    def generate_card_number(self):
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(CARD_LENGTH - len(CARD_PREFIX) - 1)])
        partial_card_number = CARD_PREFIX + account_number
        checksum = self.calculate_luhn_checksum(partial_card_number)
        return partial_card_number + str(checksum)

    @staticmethod
    def generate_pin(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(PIN_LENGTH)])

    @staticmethod
    def generate_cvv(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])

    @staticmethod
    def calculate_luhn_checksum(self, partial_card_number):
        digits = [int(d) for d in partial_card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d * 2))
        return (10 - (checksum % 10)) % 10