import pytest
from banking_core.services.account_manager import AccountManager

@pytest.fixture
def account_manager():
    return AccountManager()

def test_create_account(account_manager):
    card_number, pin = account_manager.create_account()
    assert len(card_number) == 16, "Card number should be 16 digits long"
    assert len(pin) == 4, "PIN should be 4 digits long"

def test_log_into_account(account_manager):
    card_number, pin = account_manager.create_account()
    success = account_manager.log_into_account(card_number, pin)
    assert success, "User should be able to log in with correct card number and PIN"

    wrong_pin = "0000"
    failure = account_manager.log_into_account(card_number, wrong_pin)
    assert not failure, "User should not be able to log in with incorrect PIN"

def test_get_balance(account_manager):
    card_number, _ = account_manager.create_account()
    balance = account_manager.get_balance(card_number)
    assert balance == 0, "New account should have a balance of 0"

def test_add_income(account_manager):
    card_number, _ = account_manager.create_account()
    account_manager.add_income(card_number, 100)
    balance = account_manager.get_balance(card_number)
    assert balance == 100, "Balance should reflect the income added"

def test_transfer(account_manager):
    source_card, _ = account_manager.create_account()
    target_card, _ = account_manager.create_account()
    account_manager.add_income(source_card, 200)

    account_manager.transfer(source_card, target_card, 50)
    source_balance = account_manager.get_balance(source_card)
    target_balance = account_manager.get_balance(target_card)
    assert source_balance == 150, "Source account balance should be reduced after transfer"
    assert target_balance == 50, "Target account balance should increase after transfer"

def test_close_account(account_manager):
    card_number, _ = account_manager.create_account()
    account_manager.close_account(card_number)
    balance = account_manager.get_balance(card_number)
    assert balance == 0, "Closed account should no longer have a balance"

def test_close_account_not_found():
    account_manager = AccountManager()
    try:
        account_manager.close_account("non_existent_card_number")
        assert False, "ValueError should be raised when account does not exist."
    except ValueError:
        pass