from banking_core.services.utils.validator import CardValidator

class TransactionValidator:
    @staticmethod
    def validate_transfer(source_card, target_card, amount, db):
        if not target_card.isdigit() or len(target_card) != 16:
            raise ValueError("Invalid card number.")

        if target_card == source_card:
            raise ValueError("Cannot transfer to the same account.")

        target_exists = db.fetch_one("SELECT * FROM card WHERE number = %s", (target_card,))
        if not target_exists:
            raise ValueError("Target account does not exist.")

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        source_balance = db.fetch_one("SELECT balance FROM card WHERE number = %s", (source_card,))
        if not source_balance or source_balance[0] < amount:
            raise ValueError("Not enough balance.")