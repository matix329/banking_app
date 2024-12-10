import random
import string
from ..utils.hasher import Hasher
import psycopg2

class CustomerCreator:
    def __init__(self, db, customer_number):
        self.db = db

    def create_customer_account(self):
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        email = input("Enter email address: ").strip()

        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty.")

        customer_number =  self.generate_customer_number()
        password = self.generate_password()
        hashed_password = Hasher.hash(password)

        try:
            query_customer = """
                INSERT INTO customer (first_name, last_name, email)
                VALUES (%s, %s, %s)
                RETURNING id;
            """

            customer_id = self.db.fetch_one(query_customer, (first_name, last_name, email))[0]

            query_account = """
                INSERT INTO account (customer_id, customer_number, password)
                VALUES (%s, %s, %s);
            """
            self.db.execute_query(query_account, (customer_id, customer_number, hashed_password))

            print("Customer account successfully created.")
            return customer_number, password

        except psycopg2.IntegrityError as e:
            self.db.connection.rollback()
            if "email" in str(e):
                print("This email is already in use.")
                raise ValueError("Email already exists.")
            else:
                print(f"Error creating customer account: {e}")
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        finally:
            self.db.connection.commit()

    def generate_customer_number(self):
        letters_part = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
        digits_part = ''.join(random.choice(string.digits) for _ in range(2))
        return letters_part + digits_part

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))