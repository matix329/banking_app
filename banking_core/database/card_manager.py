from ..database.base_manager import BaseManager

class CardManager(BaseManager):
    def lock_account(self, card_number):
        if not card_number or card_number.strip() == "":
            raise ValueError("Invalid card number")
        self.execute_query('''UPDATE card SET locked = TRUE WHERE number = %s''', (card_number,))

    def unlock_account(self, card_number):
        if not card_number or card_number.strip() == "":
            raise ValueError("Invalid card number")
        self.execute_query('''UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = %s''', (card_number,))
