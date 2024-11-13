from banking_core.services.account_manager import AccountManager

def main():
    account_manager = AccountManager()
    while True:
        print("1. Create an account\n2. Log into account\n0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            card_number, pin = account_manager.create_account()
            print("Your card has been created")
            print(f"Your card number:\n{card_number}")
            print(f"Your card PIN:\n{pin}")
        elif choice == '2':
            card_number = input("Enter your card number: ")
            pin = input("Enter your PIN: ")
            if account_manager.log_into_account(card_number, pin):
                print("You have successfully logged in!")
                while True:
                    print("1. Balance\n2. Add income\n3. Do transfer\n4. Transaction history\n5. Close account\n6. Log out\n0. Exit")
                    inner_choice = input("Choose an option: ")

                    if inner_choice == '1':
                        print(f"Balance: {account_manager.get_balance(card_number)}")
                    elif inner_choice == '2':
                        income = int(input("Enter income: "))
                        account_manager.add_income(card_number, income)
                    elif inner_choice == '3':
                        target_card = input("Enter card number: ")
                        amount = int(input("Enter amount: "))
                        try:
                            account_manager.transfer(card_number, target_card, amount)
                            print("Success!")
                        except ValueError as e:
                            print(e)
                    elif inner_choice == '4':
                        print("Transaction history:")
                        account_manager.get_transaction_history(card_number)
                    elif inner_choice == '5':
                        account_manager.close_account(card_number)
                        break
                    elif inner_choice == '6':
                        print("You have successfully logged out!")
                        break
                    elif inner_choice == '0':
                        print("Bye!")
                        return
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Wrong card number or PIN!")
        elif choice == '0':
            print('Bye!')
            break
        else:
            print("Invalid choice. Please select from the menu options.")

if __name__ == "__main__":
    main()