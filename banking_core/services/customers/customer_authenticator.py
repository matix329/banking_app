class CustomerAuthenticator:
    def __init__(self, db, password_hasher):
        self.db = db
        self.password_hasher = password_hasher

    def log_into_customer_account(self, customer_number, password):
        result = self.db.fetch_one(
            "SELECT id, password FROM account WHERE customer_number = %s",
            (customer_number,))

        if result:
            stored_customer_id, stored_hash = result

            if self.password_hasher.check(stored_hash, password):
                return True
            else:
                raise ValueError("Incorrect password.")
        else:
            raise ValueError("Customer account not found.")