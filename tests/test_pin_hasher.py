import pytest
from banking_core.services.pin_hasher import PinHasher

def test_pin_hashing():
    pin = "1234"
    hashed_pin = PinHasher.hash_pin(pin)

    assert PinHasher.check_pin(hashed_pin, pin) == True
    assert PinHasher.check_pin(hashed_pin, "wrong_pin") == False