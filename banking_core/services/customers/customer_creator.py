import random
import string
from ..utils.hasher import Hasher


class CustomerCreator:
    def __init__(self, db, customer_number):
        self.db = db
        self.customer_number = customer_number

    def create_customer_account(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email address: ")  # Pobieranie adresu e-mail

        while True:
            customer_number = self.generate_customer_number()
            if not self.db.fetch_one("SELECT customer_number FROM account WHERE customer_number = %s",
                                     (customer_number,)):
                break

        password = self.generate_password()
        hashed_password = Hasher.hash(password)

        customer_id = self.generate_customer_id()

        self.db.execute_query(
            "INSERT INTO customer (id, first_name, last_name, email) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (customer_id, first_name, last_name, email)
        )
        self.db.execute_query(
            "INSERT INTO account (customer_id, customer_number, password) VALUES (%s, %s, %s)",
            (customer_id, customer_number, hashed_password)
        )
        return customer_number, password

    def get_customer_number(self):
        customer_id = input("Enter customer number: ")
        return customer_id

    def generate_customer_number(self):
        letters_part = [random.choice(string.ascii_letters) for _ in range(5)]
        digits_part = [random.choice(string.digits) for _ in range(2)]
        account_number = letters_part + digits_part
        random.shuffle(account_number)
        return ''.join(account_number)

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_customer_id(self):
        return random.randint(1, 999999)