import random

class AccountCreator:
    def __init__(self, db, customer_number):
        self.db = db
        self.customer_number = customer_number
        self.account_id = self.get_customer_number()

    def create_account(self):
        customer_number = self.customer_number

        try:
            query = "SELECT 1 FROM account WHERE customer_number = %s;"
            customer_exists = self.db.fetch_one(query, (self.account_id,))
            if not customer_exists:
                print(f"No account found for customer_number: {customer_number}.")
                return {
                    "success": False,
                    "message": f"No account found for {customer_number}."
                }

            valid_currencies = ["USD", "EUR", "PLN"]
            currency = input("Enter currency (USD, EUR, PLN): ").strip().upper()

            if currency not in valid_currencies:
                print("This currency is not available. Defaulting to USD.")
                currency = "USD"

            existing_subaccount = self.check_existing_currency(currency)
            if existing_subaccount:
                query = """ SELECT id, account_number, currency, balance FROM sub_account WHERE account_id = %s AND currency = %s; """
                subaccount_data = self.db.fetch_one(query, (self.account_id, currency))
                print(f"Sub account for currency {currency} already exists. Proceeding without creating a new one.")
                return {
                    "success": True,
                    "sub_account_id": subaccount_data[0],
                    "account_number": subaccount_data[1],
                    "currency": subaccount_data[2],
                    "balance": float(subaccount_data[3])
                }

            account_number = self.generate_account_number()

            query = """
            INSERT INTO sub_account (account_id, account_number, currency, balance)
            VALUES (%s, %s, %s, 0)
            RETURNING id, account_number, currency, balance;
            """
            result = self.db.fetch_one(query, (customer_number, account_number, currency))

            if not result:
                print("Sub account creation failed. No data returned from query.")
                return {
                    "success": False,
                    "message": "Sub account creation failed. No result returned."
                }

            return {
                "success": True,
                "sub_account_id": result[0],
                "account_number": result[1],
                "currency": result[2],
                "balance": float(result[3])
            }
        except Exception as e:
            print(f"Error encountered: {e}. Review the input and retry.")
            raise

    def check_existing_currency(self, currency):
        query = """
        SELECT 1
        FROM sub_account
        WHERE account_id = %s AND currency = %s;
        """
        result = self.db.fetch_one(query, (self.account_id, currency))
        return result is not None

    def generate_account_number(self):
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(26)])
            if not self.db.fetch_one("SELECT 1 FROM sub_account WHERE account_number = %s", (account_number,)):
                return account_number


    def get_customer_number(self):
        query = """
            SELECT customer_number
            FROM account
            WHERE customer_number = %s;
        """
        result = self.db.fetch_one(query, (self.customer_number,))
        if not result:
            raise ValueError(f"No account found for customer number: {self.customer_number}")
        return result[0]