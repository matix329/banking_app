import random
from banking_core.services.validator import is_valid_card_number, luhn_checksum
from banking_core.database.db_manager import DatabaseManager

class AccountManager:
    def __init__(self):
        self.db = DatabaseManager()

    def create_account(self):
        card_number = self.generate_card_number()
        pin = self.generate_pin()
        self.db.execute_query("INSERT INTO card (number, pin, balance) VALUES (?, ?, 0)", (card_number, pin))
        return card_number, pin

    def generate_card_number(self):
        iin = "400000"
        acc_number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        partial_card_number = iin + acc_number
        check_digit = (10 - luhn_checksum(int(partial_card_number + "0"))) % 10
        return partial_card_number + str(check_digit)

    def generate_pin(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def log_into_account(self, card_number, pin):
        result = self.db.fetch_one("SELECT number FROM card WHERE number = ? AND pin = ?", (card_number, pin))
        return result is not None

    def get_balance(self, card_number):
        result = self.db.fetch_one("SELECT balance FROM card WHERE number = ?", (card_number,))
        return result[0] if result else 0

    def add_income(self, card_number, income):
        self.db.execute_query("UPDATE card SET balance = balance + ? WHERE number = ?", (income, card_number))

    def transfer(self, source_card, target_card, amount):
        if not is_valid_card_number(target_card):
            raise ValueError("Invalid card number.")
        if self.get_balance(source_card) < amount:
            raise ValueError("Not enough balance.")
        self.db.execute_query('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, source_card))
        self.db.execute_query('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, target_card))

        self.record_transaction(source_card, "transfer_out", -amount)
        self.record_transaction(target_card, "transfer_in", amount)

    def close_account(self, card_number):
        self.db.execute_query("DELETE FROM card WHERE number = ?", (card_number,))

    def record_transaction(self, account_number, transaction_type, amount):
        self.db.execute_query(
            "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (?, ?, ?)",
            (account_number, transaction_type, amount)
        )

    def get_transaction_history(self, card_number):
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT date, transaction_type, amount FROM transactions WHERE account_number = ? ORDER BY date DESC",
            (card_number,))
        transactions = cursor.fetchall()

        if transactions:
            for transaction in transactions:
                print(f"Date: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]}")
        else:
            print("No transactions found for this account.")