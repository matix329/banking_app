import pytest
from argon2 import PasswordHasher
from banking_core.services.utils.hasher import Hasher

def test_hash_pin():
    pin_to_hash = '1234'
    hashed_pin = Hasher.hash(pin_to_hash)
    assert isinstance(hashed_pin, str), "hash_pin must return a string"
    assert hashed_pin.startswith("$argon2id$"), "Hashed PIN should start with $argon2id$"

def test_check_pin():
    ph = PasswordHasher()
    hardcoded_pin = '1234'
    stored_hash = ph.hash(hardcoded_pin)
    assert Hasher.check(stored_hash, hardcoded_pin), "check_pin must return True for correct pin"
    wrong_pin = '9999'
    assert not Hasher.check(stored_hash, wrong_pin), "check_pin must return False for incorrect pin"

def test_check_pin_string():
    ph = PasswordHasher()
    stored_hash = ph.hash('1234')
    stored_hash_str = stored_hash
    assert Hasher.check(stored_hash_str, '1234'), "check_pin must return True for correct pin and string stored_hash"

def test_check_pin_value_error():
    invalid_stored_hash_str = "Invalid string"
    assert not Hasher.check(invalid_stored_hash_str, '1234')
