import pytest
from unittest.mock import MagicMock
from banking_core.database.card_manager import CardManager

INVALID_CARD_NUMBERS = [None, "", " "]
VALID_CARD_NUMBER = ["1234567812345678"]

@pytest.fixture
def card_manager():
    mock_connection = MagicMock()
    return CardManager(mock_connection)

def assert_raises_exception(card_manager, action, card_number):
    with pytest.raises(ValueError):
        action(card_manager, card_number)

def assert_not_raises_exception(card_manager, action, card_number):
    try:
        action(card_manager, card_number)
    except:
        pytest.fail(f"{action.__name__} raised Exception unexpectedly!")

@pytest.mark.parametrize("card_number", INVALID_CARD_NUMBERS)
def test_lock_account_with_invalid_card_number_raises_exception(card_manager, card_number):
    assert_raises_exception(card_manager, CardManager.lock_account, card_number)

@pytest.mark.parametrize("card_number", VALID_CARD_NUMBER)
def test_lock_account_with_valid_card_number_not_raises_exception(card_manager, card_number):
    assert_not_raises_exception(card_manager, CardManager.lock_account, card_number)

@pytest.mark.parametrize("card_number", INVALID_CARD_NUMBERS)
def test_unlock_account_with_invalid_card_number_raises_exception(card_manager, card_number):
    assert_raises_exception(card_manager, CardManager.unlock_account, card_number)

@pytest.mark.parametrize("card_number", VALID_CARD_NUMBER)
def test_unlock_account_with_valid_card_number_not_raises_exception(card_manager, card_number):
    assert_not_raises_exception(card_manager, CardManager.unlock_account, card_number)