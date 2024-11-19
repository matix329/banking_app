from banking_core.services import PinHasher

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