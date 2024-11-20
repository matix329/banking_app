from unittest import result
import pytest
from unittest.mock import MagicMock
from banking_core.services import AccountCreator, AccountAuthenticator, AccountLocker, PinHasher

@pytest.fixture
def mocked_db():
    return MagicMock()

@pytest.fixture
def account_locker(mocked_db):
    return AccountLocker(mocked_db)

@pytest.fixture
def account_authenticator(mocked_db, account_locker):
    return AccountAuthenticator(mocked_db, PinHasher(), account_locker)

@pytest.fixture
def account_creator(mocked_db):
    return AccountCreator(mocked_db)

def test_log_into_account_success(account_authenticator, mocked_db):
    card_number = "4000001234567890"
    pin = "1234"
    hashed_pin = PinHasher.hash_pin(pin)

    mocked_db.fetch_one.return_value = (card_number, hashed_pin, 0, False)
    success = account_authenticator.log_into_account(card_number, pin)

    assert success
    mocked_db.fetch_one.assert_called_once_with(
        "SELECT number, pin, failed_attempts, locked FROM card WHERE number = %s", (card_number,)
    )

def test_log_into_account_failure_wrong_pin(account_authenticator, mocked_db):
    card_number = "4000001234567890"
    wrong_pin = "0000"
    hashed_pin = PinHasher.hash_pin("1234")

    mocked_db.fetch_one.return_value = (card_number, hashed_pin, 0, True)
    with pytest.raises(ValueError, match="Your account is already locked."):
        account_authenticator.log_into_account(card_number, wrong_pin)

def test_log_into_account_failure_nonexistent_account(account_authenticator, mocked_db):
    card_number = "4000001234567890"

    mocked_db.fetch_one.return_value = None
    with pytest.raises(ValueError, match="Account not found."):
        account_authenticator.log_into_account(card_number, "1234")

def test_unlock_account_success(account_locker, mocked_db):
    card_number = "4000001234567890"

    mocked_db.fetch_one.return_value = (False,)
    with pytest.raises(ValueError, match="This account is not locked."):
        account_locker.unlock_account(card_number)

def test_lock_account_already_locked(account_locker, mocked_db):
    card_number = "4000001234567890"

    mocked_db.fetch_one.return_value = (0, True)
    with pytest.raises(ValueError, match="Your account is already locked."):
        account_locker.lock_account_after_failed_attempt(card_number)

def test_lock_account_nonexistent(account_locker, mocked_db):
    card_number = "4000001234567890"

    mocked_db.fetch_one.return_value = None
    if not result:
        raise ValueError("Account not found.")

def test_multiple_failed_login_attempts(account_authenticator, mocked_db):
    card_number = "4000001234567890"
    pin = "1234"
    hashed_pin = PinHasher.hash_pin(pin)

    mocked_db.fetch_one.side_effect = [
        (card_number, hashed_pin, 0, False),
        (card_number, hashed_pin, 1, False),
        (card_number, hashed_pin, 2, False),
        (card_number, hashed_pin, 3, True),
    ]
    with pytest.raises(ValueError, match="Your account is already locked."):
        account_authenticator.log_into_account(card_number, "wrong_pin")