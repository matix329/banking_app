import pytest
from banking_core.services.utils.validator import CardValidator

def test_luhn_checksum():
    assert CardValidator.luhn_checksum('378282246310005') == 0
    assert CardValidator.luhn_checksum('371449635398431') == 0
    assert CardValidator.luhn_checksum('5555555555554444') == 0
    assert CardValidator.luhn_checksum('4111111111111111') == 0
    assert CardValidator.luhn_checksum('1234567890123456') != 0

def test_is_valid_card_number():
    assert CardValidator.is_valid_card_number('378282246310005') is False
    assert CardValidator.is_valid_card_number('371449635398431') is False
    assert CardValidator.is_valid_card_number('5555555555554444') is True
    assert CardValidator.is_valid_card_number('4111111111111111') is True
    assert CardValidator.is_valid_card_number('1234567890123456') is False
    assert CardValidator.is_valid_card_number('1111222233334444') is True
    assert CardValidator.is_valid_card_number('abcdefghi') is False
    assert CardValidator.is_valid_card_number(1234567890123456) is False