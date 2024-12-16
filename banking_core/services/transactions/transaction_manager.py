from banking_core.services.transactions.transaction_validator import TransactionValidator

class TransactionManager:
    def __init__(self, db):
        self.db = db

    def transfer(self, source_sub_account_id, target_sub_account_id, amount):
        TransactionValidator.validate_transfer(source_sub_account_id, target_sub_account_id, amount, self.db)

        try:
            self.db.execute_query(
                "UPDATE sub_account SET balance = balance - %s WHERE id = %s",
                (amount, source_sub_account_id)
            )

            self.db.execute_query(
                "UPDATE sub_account SET balance = balance + %s WHERE id = %s",
                (amount, target_sub_account_id)
            )
            self.record_transaction(source_sub_account_id, "transfer_out", -amount)
            self.record_transaction(target_sub_account_id, "transfer_in", amount)

            print("Transfer successful!")
        except Exception as e:
            raise RuntimeError(f"Transfer failed: {e}")

    def add_income(self, sub_account_id, income):
        if not isinstance(income, (int, float)) or income <= 0:
            raise ValueError("Income must be a positive number.")

        result = self.db.fetch_one(
            "UPDATE sub_account SET balance = balance + %s WHERE account_number = %s RETURNING balance;",
            (income, sub_account_id)
        )

        if not result:
            raise ValueError("Failed to add income. Account not found or invalid account number.")

        new_balance = result[0]
        print(f"Income of {income:.2f} has been added to your account.")
        print(f"Your new balance is: {new_balance:.2f}")
        return new_balance

    def get_transaction_history(self, sub_account_id):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT date, transaction_type, amount FROM transactions WHERE account_id = %s ORDER BY date DESC",
            (sub_account_id,))
        transactions = cursor.fetchall()

        if transactions:
            for transaction in transactions:
                print(f"Date: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]}")
        else:
            print("No transactions found for this account.")

    def record_transaction(self, sub_account_id, transaction_type, amount):
        query = """
            INSERT INTO transactions (account_id, transaction_type, amount, date)
            VALUES (%s, %s, %s, NOW())
        """
        self.db.execute_query(query, (sub_account_id, transaction_type, amount))

    def get_balance(self, sub_account_id):
        result = self.db.fetch_one("SELECT balance FROM sub_account WHERE account_number = %s", (sub_account_id,))
        return result[0] if result else 0.0