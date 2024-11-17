import pytest
from banking_core.services.account_manager import AccountManager
from unittest.mock import MagicMock, patch

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


def test_lock_account_after_failed_attempt(account_manager):
    account_manager.db = MagicMock()

    account_manager.db.fetch_one.side_effect = [
        (1, False),
        (2, False),
        (3, False),
        (3, True)
    ]

    card_number = "4000001234567890"

    account_manager.lock_account_after_failed_attempt(card_number)
    account_manager.lock_account_after_failed_attempt(card_number)

    with pytest.raises(ValueError, match="Your account has been locked due to multiple failed login attempts."):
        account_manager.lock_account_after_failed_attempt(card_number)

    account_manager.db.execute_query.assert_any_call(
        "UPDATE card SET locked = 1 WHERE number = ?", (card_number,)
    )

    with pytest.raises(ValueError, match="Your account is already locked."):
        account_manager.lock_account_after_failed_attempt(card_number)

def test_account_locked(account_manager):
    card_number, pin = account_manager.create_account()

    with patch.object(account_manager.db, 'fetch_one', return_value=(card_number, 'hashedpin', 3, True)):
        with pytest.raises(ValueError, match="This account is locked due to multiple failed login attempts."):
            account_manager.log_into_account(card_number, pin)


def test_hash_pin(account_manager):
    pin = "1234"
    hashed_pin = account_manager.hash_pin(pin)

    assert hashed_pin != pin, "Hashed PIN should not be equal to the original PIN"

    assert account_manager.check_pin(hashed_pin, pin), "The PIN does not match the hash"