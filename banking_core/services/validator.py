def luhn_checksum(card_number):
    digits = [int(d) for d in str(card_number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(int(x) for x in str(d * 2))
    return checksum % 10

def is_valid_card_number(card_number):
    return len(card_number) == 16 and luhn_checksum(card_number) == 0