from banking_core.services.utils.validator import CardValidator

class TransactionValidator:
    @staticmethod
    def validate_transfer(source_sub_account_id, target_sub_account_id, amount, db):
        if not isinstance(target_sub_account_id, int) or target_sub_account_id <= 0:
            raise ValueError("Invalid account ID.")

        if target_sub_account_id == source_sub_account_id:
            raise ValueError("Cannot transfer to the same account.")

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        target_exists = db.fetch_one("SELECT * FROM sub_account WHERE id = %s", (target_sub_account_id,))
        if not target_exists:
            raise ValueError("Target account does not exist.")

        source_balance = db.fetch_one("SELECT balance FROM sub_account WHERE id = %s", (source_sub_account_id,))
        if not source_balance or source_balance[0] < amount:
            raise ValueError("Not enough balance.")

        daily_limit_row = db.fetch_one("SELECT daily_limit FROM daily_limits WHERE sub_account_id = %s",
                                       (source_sub_account_id,))

        if daily_limit_row:
            daily_limit = daily_limit_row[0]
            total_transferred_today = db.fetch_one(
                """
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE account_id = %s 
                AND DATE(date) = DATE(NOW())
                """,
                (source_sub_account_id,)
            )[0]

            if total_transferred_today + amount > daily_limit:
                raise ValueError("Transfer amount exceeds daily limit.")