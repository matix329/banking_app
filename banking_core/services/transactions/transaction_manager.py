from banking_core.services.transactions.transaction_validator import TransactionValidator

class TransactionManager:
    def __init__(self, db):
        self.db = db

    def transfer(self, source_card, target_card, amount):
        TransactionValidator.validate_transfer(source_card, target_card, amount, self.db)

        try:

            self.db.execute_query(
                "UPDATE card SET balance = balance - %s WHERE number = %s",
                (amount, source_card)
            )

            self.db.execute_query(
                "UPDATE card SET balance = balance + %s WHERE number = %s",
                (amount, target_card)
            )

            self.record_transaction(source_card, "transfer_out", -amount)
            self.record_transaction(target_card, "transfer_in", amount)

            print("Transfer successful!")
        except Exception as e:
            raise RuntimeError(f"Transfer failed: {e}")

    def add_income(self, card_number, income):
        if not isinstance(income, int) or income <= 0:
            raise ValueError("Income must be a positive number.")
        self.db.execute_query("UPDATE card SET balance = balance + %s WHERE number = %s", (income, card_number))
        print(f"Income of {income} has been added to your account.")

    def get_transaction_history(self, card_number):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT date, transaction_type, amount FROM transactions WHERE account_number = %s ORDER BY date DESC",
            (card_number,))
        transactions = cursor.fetchall()

        if transactions:
            for transaction in transactions:
                print(f"Date: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]}")
        else:
            print("No transactions found for this account.")