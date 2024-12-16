from banking_core.services import AccountCreator, AccountAuthenticator, AccountLocker, TransactionManager, \
    CustomerCreator, CustomerAuthenticator, LimitManager, Hasher
from banking_core.database import *
from banking_core.database import setup_database as setup

def main_menu_logic(account_authenticator, transaction_manager, account_locker, limit_manager, db_manager, customer_number):
    def main_menu():
        print("1. Create an account\n2. Log into account\n0. Exit")

    def account_menu():
        print(
            "1. Balance\n2. Add income\n3. Do transfer\n4. Transaction history\n5. Close account\n6. Set daily limit\n7. Add new exchange account\n8. Exchange currency\n9. Change password\n10. Log out\n0. Exit")

    account_creator = None

    while True:
        main_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                if account_creator is None:
                    account_creator = AccountCreator(db_manager, customer_number)

                account_details = account_creator.create_account()
                print("Your sub account has been created")
                print(f"Your sub account number:\n{account_details['account_number']}")
            except Exception as e:
                print(f"Failed to create sub account: {e}")

        elif choice == '2':
            try:
                selected_account =  account_authenticator.log_into_account(customer_number)
                if selected_account is not None:
                    print("You have successfully logged in!")
                    account_number =  selected_account[0]
                    currency  = selected_account[1]

                    while True:
                        account_menu()
                        inner_choice = input("Choose an option: ")

                        if inner_choice == '1':
                            balance = transaction_manager.get_balance(account_number)
                            print(f"Your balance is: {balance:.2f} {currency}")

                        elif inner_choice == '2':
                            try:
                                income  = float(input("Enter income: "))
                                transaction_manager.add_income(account_number, income)
                            except ValueError as e:
                                print(f"Error: {e} Please enter a valid positive number")

                        elif inner_choice == '3':
                            print("The feature will be added soon.")

                        elif inner_choice == '4':
                            print("The feature will be added soon.")

                        elif inner_choice == '5':
                            print("The feature will be added soon.")

                        elif inner_choice == '6':
                            print("The feature will be added soon.")

                        elif inner_choice == '7':
                            print("The feature of adding new accounts will be added soon.")

                        elif inner_choice == '8':
                            print("Currency exchange feature will be added soon.")

                        elif inner_choice == '9':
                            print("Password change feature will be added soon.")

                        elif inner_choice == '10':
                            print("You have successfully logged out!")
                            break

                        elif inner_choice == '0':
                            print("Bye!")
                            return

                        else:
                            print("Invalid option. Please try again.")

                else:
                    print("Failed to log into any account.")

            except ValueError as e:
                print(e)

        elif choice == '0':
            print('Bye!')
            break

        else:
            print("Invalid choice. Please select from the menu options.")

def main():
    db_connection = DatabaseConnection()
    setup(db_connection.get_connection())
    db_manager = BaseManager(db_connection.get_connection())
    hasher = Hasher()
    account_locker = AccountLocker(db_manager)
    account_authenticator = AccountAuthenticator(db_manager, None)
    customer_creator = CustomerCreator(db_manager, None)
    customer_authenticator = CustomerAuthenticator(db_manager, hasher)
    transaction_manager = TransactionManager(db_manager)
    limit_manager = LimitManager(db_manager)

    def logon_menu():
        print("Do you have customer account?\n1. Log in\n2. Create a customer account\n0. Exit")

    while True:
        logon_menu()
        option = input("Choose an option: ")

        if option == '1':
            customer_number = input("Enter your customer number: ")
            password = input("Enter your password: ")
            try:
                if customer_authenticator.log_into_customer_account(customer_number, password):
                    print("You have successfully logged in!")
                    main_menu_logic(account_authenticator, transaction_manager, account_locker, limit_manager,
                                    db_manager,
                                    customer_number)
            except ValueError as e:
                print(e)

        elif option == '2':
            customer_number, password = customer_creator.create_customer_account()
            print("Client account created successfully!")
            print(f"Your customer number:\n{customer_number}")
            print(f"Your password:\n{password}")

        elif option == '0':
            print('Bye!')
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()