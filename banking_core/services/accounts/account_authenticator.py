class AccountAuthenticator:
    def __init__(self, db, customer_number):
        self.db = db
        self.customer_number = customer_number

    def log_into_account(self, account_id):
        accounts = self.db.fetch_all(
            "SELECT account_number, currency FROM sub_account WHERE account_id = %s LIMIT 3",
            (account_id,)
        )
        selected_account = self.display_accounts(accounts)
        if selected_account:
            print(f"You have selected account {selected_account[0]} with currency {selected_account[1]}")
            return selected_account
        else:
            print("No account selected.")
            return None

    def display_accounts(self, accounts):
        if not accounts:
            print("No accounts available.")
            return None

        print("\nAvailable accounts:")
        for idx, (account_number, currency) in enumerate(accounts, start=1):
            print(f"{idx}. Account Number: {account_number} | Currency: {currency}")

        while True:
            try:
                choice = int(input("\nSelect an account by number (1-3): "))
                if 1 <= choice <= len(accounts):
                    return accounts[choice - 1]
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")