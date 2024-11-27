class CardValidator:
    @staticmethod
    def luhn_checksum(card_number):
        digits = [int(d) for d in str(card_number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d * 2))
        return checksum % 10

    @staticmethod
    def is_valid_card_number(card_number):
        if not isinstance(card_number, str) or not card_number.isdigit():
            return False
        if len(card_number) != 16:
            return False
        return CardValidator.luhn_checksum(card_number) == 0

class InputValidator:
    @staticmethod
    def get_positive_number(prompt):
        while True:
            try:
                user_input = float(input(prompt))
                if user_input > 0 and round(user_input * 100) == user_input * 100:
                    return user_input
                else:
                    print("Please enter a positive number with a maximum of two decimal places.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")