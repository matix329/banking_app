from banking_core.services.validator import luhn_checksum, is_valid_card_number

def test_luhn_checksum_valid():
    valid_card_number = "4000001234567890"
    assert luhn_checksum(valid_card_number) == 0, "Checksum should be 0 for a valid card number"

def test_luhn_checksum_invalid():
    invalid_card_number = "4000001234567891"
    assert luhn_checksum(invalid_card_number) != 0, "Checksum should not be 0 for an invalid card number"

def test_is_valid_card_number():
    valid_card_number = "4000001234567890"
    assert is_valid_card_number(valid_card_number), "The card number should be valid"

def test_is_invalid_card_number_length():
    short_card_number = "40000012345678"
    assert not is_valid_card_number(short_card_number), "Card number with incorrect length should be invalid"

def test_is_invalid_card_number_checksum():
    invalid_card_number = "4000001234567891"
    assert not is_valid_card_number(invalid_card_number), "Card number with invalid checksum should be invalid"
