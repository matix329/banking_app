import random
from banking_core.services.validator import is_valid_card_number, luhn_checksum
from banking_core.database.db_manager import DatabaseManager
from datetime import datetime
import bcrypt

class AccountManager:
    def __init__(self):
        self.db = DatabaseManager()

    def create_account(self):
        while True:
            card_number = self.generate_card_number()
            if not self.db.fetch_one("SELECT number FROM card WHERE number = ?", (card_number,)):
                break

        pin = self.generate_pin()
        hashed_pin = self.hash_pin(pin)

        self.db.execute_query("INSERT INTO card (number, pin, balance) VALUES (?, ?, 0)", (card_number, hashed_pin))
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
        result = self.db.fetch_one("SELECT number, pin, failed_attempts, locked FROM card WHERE number = ?", (card_number,))

        if result:
            stored_card_number, stored_hash, failed_attempts, locked = result

            if locked:
                raise ValueError("This account is locked due to multiple failed login attempts.")

            elif self.check_pin(stored_hash, pin):
                self.db.execute_query("UPDATE card SET failed_attempts = 0 WHERE number = ?", (card_number,))
                return True
            else:
                self.lock_account_after_failed_attempt(card_number)

        return False

    def get_balance(self, card_number):
        result = self.db.fetch_one("SELECT balance FROM card WHERE number = ?", (card_number,))
        return result[0] if result else 0

    def add_income(self, card_number, income):
        if not isinstance(income, int) or income <= 0:
            raise ValueError("Income must be a positive number.")
        self.db.execute_query("UPDATE card SET balance = balance + ? WHERE number = ?", (income, card_number))
        print(f"Income of {income} has been added to your account.")

    def transfer(self, source_card, target_card, amount):
        try:
            if not target_card.isdigit() or len(target_card) != 16:
                raise ValueError("Invalid card number.")

            if target_card == source_card:
                raise ValueError("Cannot transfer to the same account.")

            target_exists = self.db.fetch_one("SELECT * FROM card WHERE number = ?", (target_card,))
            if not target_exists:
                raise ValueError("Target account does not exist.")

            if amount <= 0:
                raise ValueError("Transfer amount must be greater than zero.")

            if self.get_balance(source_card) < amount:
                raise ValueError("Not enough balance.")

            self.db.execute_query('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, source_card))
            self.db.execute_query('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, target_card))

            self.record_transaction(source_card, "transfer_out", -amount)
            self.record_transaction(target_card, "transfer_in", amount)
            print("Success!")
        except ValueError as e:
            print(e)
            raise
        except Exception as e:
            print("Unexpected error occurred:", e)
            raise

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

        if self.check_pin(stored_pin, pin):
            try:
                new_limit = int(input("Enter your new daily transaction limit: "))
                if new_limit <= 0:
                    raise ValueError("Daily limit must be greater than zero.")
            except ValueError as ve:
                raise ve
            except Exception:
                raise ValueError("Invalid input. Please enter a valid number.")

            if limit_data:
                self.db.update_daily_limit(card_number, new_limit)
            else:
                self.db.add_daily_limit(card_number, new_limit)

            print(f"Your daily limit has been set to {new_limit}.")
        else:
            print("Invalid PIN.")

    def lock_account_after_failed_attempt(self, card_number):
        self.db.execute_query("UPDATE card SET failed_attempts = failed_attempts + 1 WHERE number = ?", (card_number,))
        result = self.db.fetch_one("SELECT failed_attempts, locked FROM card WHERE number = ?", (card_number,))

        if not result:
            raise ValueError("Account not found.")

        failed_attempts = result[0]
        locked = result[1]

        if locked:
            raise ValueError("Your account is already locked.")

        if failed_attempts >= 3:
            self.db.execute_query("UPDATE card SET locked = 1 WHERE number = ?", (card_number,))
            raise ValueError("Your account has been locked due to multiple failed login attempts.")

    def unlock_account(self, card_number):
        self.db.execute_query("UPDATE card SET locked = FALSE, failed_attempts = 0 WHERE number = ?", (card_number,))
        print("The account has been unlocked.")

    def hash_pin(self, pin):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pin.encode('utf-8'), salt)
        return hashed

    def check_pin(self, stored_hash, entered_pin):
        return bcrypt.checkpw(entered_pin.encode('utf-8'), stored_hash)