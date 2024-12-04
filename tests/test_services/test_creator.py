import pytest
import random
from unittest.mock import Mock
from banking_core.services import CARD_PREFIX, CARD_LENGTH, PIN_LENGTH, AccountCreator, Hasher
from dotenv import load_dotenv
import os
from bcrypt import hashpw

load_dotenv()

TEST_SALT = os.getenv("TEST_SALT").encode('utf-8')

class TestHasher(Hasher):
    def __init__(self):
        super().__init__()

    def hash(self, pin):
        return hashpw(pin.encode('utf-8'), TEST_SALT)

@pytest.fixture
def mock_database():
    return Mock()

@pytest.fixture
def mock_account_creator(mock_database):
    return AccountCreator(mock_database)

@pytest.fixture
def pinhash():
    return TestHasher()

def assert_card_number(card_number):
    assert len(card_number) == CARD_LENGTH
    assert card_number[:len(CARD_PREFIX)] == CARD_PREFIX
    assert card_number[len(CARD_PREFIX):-1].isdigit()
    assert 0 <= int(card_number[-1]) <= 9

def assert_pin(pin):
    assert len(pin) == PIN_LENGTH
    assert pin.isdigit()

def test_generate_card_number(mock_account_creator):
    card_number = mock_account_creator.generate_card_number()
    assert_card_number(card_number)

def test_generate_pin(mock_account_creator):
    pin = mock_account_creator.generate_pin()
    assert_pin(pin)

def test_calculate_luhn_checksum(mock_account_creator):
    partial_number = "400000123456789"
    checksum = mock_account_creator.calculate_luhn_checksum(partial_card_number=partial_number)
    assert isinstance(checksum, int)
    assert 0 <= checksum < 10


def test_create_account(mock_account_creator, mock_database, pinhash):
    db_mock = mock_database
    db_mock.fetch_one.return_value = None
    card_number, pin = mock_account_creator.create_account()
    assert_card_number(card_number)
    assert_pin(pin)
    db_mock.fetch_one.assert_any_call("SELECT number FROM card WHERE number = %s", (card_number,))
    hashed_pin = pinhash.hash(pin)
    args, kwargs = db_mock.execute_query.call_args
    assert args[0] == "INSERT INTO card (number, pin, balance) VALUES (%s, %s, 0)"
    assert args[1][0] == card_number
    assert args[1][1].startswith("$argon2id$")