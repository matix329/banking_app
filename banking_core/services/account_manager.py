import random
from banking_core.services.validator import is_valid_card_number, luhn_checksum
from banking_core.database.db_manager import DatabaseManager
from datetime import datetime

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

        limit_data = self.db.get_daily_limit(source_card)
        if limit_data:
            daily_limit = limit_data[0]
            changes_today = limit_data[1]
            set_date = limit_data[2]

            if amount > daily_limit:
                raise ValueError(f"Transaction denied: You cannot exceed your daily limit of {daily_limit}.")

            if changes_today >= 3:
                raise ValueError("You have reached the maximum number of changes for today. Try again tomorrow.")

        self.db.execute_query('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, source_card))
        self.db.execute_query('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, target_card))

        self.record_transaction(source_card, "transfer_out", -amount)
        self.record_transaction(target_card, "transfer_in", amount)

    def close_account(self, card_number):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM card WHERE number = ?", (card_number,))
        if cursor.fetchone() is None:
            raise ValueError("Account does not exist.")
        self.db.execute_query("DELETE FROM card WHERE number = ?", (card_number,))
        print("The account has been closed!")

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

    def set_daily_limit(self, card_number):
        limit_data = self.db.get_daily_limit(card_number)

        if limit_data:
            daily_limit = limit_data[0]
            changes_today = limit_data[1]
            set_date = limit_data[2]

            print(f"Current daily limit: {daily_limit}, Changes today: {changes_today}, Set on: {set_date}")

            if limit_data[2] == str(datetime.now().date()) and changes_today >= 3:
                print("You have reached the maximum number of changes for today. Try again tomorrow.")
                return
        else:
            print("No daily limit set for this account.")

        pin = input("Enter your PIN to confirm: ")
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT pin FROM card WHERE number = ?", (card_number,))
        stored_pin = cursor.fetchone()[0]

        if pin == stored_pin:
            new_limit = int(input("Enter your new daily transaction limit: "))

            if limit_data:
                self.db.update_daily_limit(card_number, new_limit)
            else:
                self.db.add_daily_limit(card_number, new_limit)

            print(f"Your daily limit has been set to {new_limit}.")
        else:
            print("Invalid PIN.")