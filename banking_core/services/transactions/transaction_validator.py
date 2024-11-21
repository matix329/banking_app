from banking_core.services.utils.validator import CardValidator

class TransactionValidator:
    @staticmethod
    def validate_transfer(source_card, target_card, amount, db):
        if not target_card.isdigit() or len(target_card) != 16:
            raise ValueError("Invalid card number.")

        if target_card == source_card:
            raise ValueError("Cannot transfer to the same account.")

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        target_exists = db.fetch_one("SELECT * FROM card WHERE number = %s", (target_card,))
        if not target_exists:
            raise ValueError("Target account does not exist.")

        source_balance = db.fetch_one("SELECT balance FROM card WHERE number = %s", (source_card,))
        if not source_balance or source_balance[0] < amount:
            raise ValueError("Not enough balance.")

        daily_limit_row = db.fetch_one("SELECT daily_limit FROM daily_limits WHERE account_number = %s", (source_card,))

        if daily_limit_row:
            daily_limit = daily_limit_row[0]
            daily_limit = -daily_limit
            total_transferred_today = db.fetch_one(
                """
                SELECT SUM(amount) 
                FROM transactions 
                WHERE account_number = %s 
                AND DATE(date) = DATE(NOW())
                """,
                (source_card,)
            )[0] or 0

            if total_transferred_today + amount < daily_limit:
                raise ValueError("Transfer amount exceeds daily limit")