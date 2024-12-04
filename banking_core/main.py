from banking_core.services import AccountCreator, AccountAuthenticator, AccountLocker, TransactionManager, \
    CustomerCreator, CustomerAuthenticator, LimitManager, InputValidator, Hasher
from banking_core.database import *
from banking_core.database import setup_database as setup

def main_menu_logic(account_creator, account_authenticator, transaction_manager, account_locker, limit_manager):
    def main_menu():
        print("1. Create an account\n2. Log into account\n0. Exit")

    def account_menu():
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Transaction history\n5. Close account\n6. Set daily limit\n7. Add new exchange account\n8. Exchange currency\n9. Log out\n0. Exit")

    while True:
        main_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            card_number, pin = account_creator.create_account()
            print("Your card has been created")
            print(f"Your card number:\n{card_number}")
            print(f"Your card PIN:\n{pin}")

        elif choice == '2':
            card_number = input("Enter your card number: ")
            pin = input("Enter your PIN: ")
            try:
                if account_authenticator.log_into_account(card_number, pin):
                    print("You have successfully logged in!")
                    while True:
                        account_menu()
                        inner_choice = input("Choose an option: ")

                        if inner_choice == '1':
                            print(f"Balance: {transaction_manager.get_balance(card_number)}")

                        elif inner_choice == '2':
                            income = InputValidator.get_positive_integer("Enter income: ")
                            transaction_manager.add_income(card_number, income)

                        elif inner_choice == '3':
                            target_card = input("Enter card number: ")
                            amount = InputValidator.get_positive_integer("Enter amount: ")
                            try:
                                transaction_manager.transfer(card_number, target_card, amount)
                            except ValueError as e:
                                print(e)

                        elif inner_choice == '4':
                            print("Transaction history:")
                            transaction_manager.get_transaction_history(card_number)

                        elif inner_choice == '5':
                            while True:
                                pin = input("Enter your PIN: ")
                                try:
                                    if account_locker.lock_account(card_number, pin):
                                        print("Account has been closed.")
                                        break
                                except ValueError as e:
                                    print(e)
                                    continue
                            break

                        elif inner_choice == '6':
                            limit_manager.set_daily_limit(card_number)

                        elif inner_choice == '7':
                            print("The feature of adding new accounts will be added soon.")

                        elif inner_choice == '8':
                            print("Currency exchange feature will be added soon.")

                        elif inner_choice == '9':
                            print("You have successfully logged out!")
                            break

                        elif inner_choice == '0':
                            print("Bye!")
                            return

                        else:
                            print("Invalid option. Please try again.")

                else:
                    print("Wrong card number or PIN!")

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
    account_authenticator = AccountAuthenticator(db_manager, hasher, account_locker)
    customer_number = None
    customer_creator = CustomerCreator(db_manager, customer_number)
    customer_number = customer_creator.generate_customer_number()
    customer_authenticator = CustomerAuthenticator(db_manager, hasher)
    account_creator = AccountCreator(db_manager, customer_number)
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
                    main_menu_logic(account_creator, account_authenticator, transaction_manager, account_locker,
                                    limit_manager)
            except ValueError as e:
                print(e)

        elif option == '2':
            customer_number, password = customer_creator.create_customer_accounnt()
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