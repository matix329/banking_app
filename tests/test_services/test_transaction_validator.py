import pytest
from banking_core.services.transactions.transaction_validator import TransactionValidator

class DummyDB:
    def fetch_one(self, sql, params):
        return self.db.get(params[0])

    def __init__(self, start_db):
        self.db = start_db

def test_invalid_target_card():
    db = DummyDB({})
    with pytest.raises(ValueError, match='Invalid card number.'):
        TransactionValidator.validate_transfer("1234567812345678", "A234567812345678", 100, db)
      
def test_same_target_source_card():
    db = DummyDB({})
    with pytest.raises(ValueError, match='Cannot transfer to the same account.'):
        TransactionValidator.validate_transfer("1234567812345678", "1234567812345678", 100, db)

def test_non_existing_target_account():
    db = DummyDB({"1234567812345678": (500,)})
    with pytest.raises(ValueError, match='Target account does not exist.'):
        TransactionValidator.validate_transfer("1234567812345678", "0000000000000000", 100, db)

def test_negative_transfer_amount():
    db = DummyDB({"1234567812345678": (500,)})
    with pytest.raises(ValueError, match='Transfer amount must be greater than zero.'):
        TransactionValidator.validate_transfer("1234567812345678", "0000000000000000", -100, db)

def test_zero_transfer_amount():
    db = DummyDB({"1234567812345678": (500,)})
    with pytest.raises(ValueError, match='Transfer amount must be greater than zero.'):
        TransactionValidator.validate_transfer("1234567812345678", "0000000000000000", 0, db)

def test_insufficient_fund_transfer():
    db = DummyDB({"1234567812345678": (500,), "0000000000000000":(0,)})
    with pytest.raises(ValueError, match='Not enough balance.'):
        TransactionValidator.validate_transfer("1234567812345678", "0000000000000000", 1000, db)
      
def test_valid_transfer():
    db = DummyDB({"1234567812345678": (1000,), "0000000000000000":(0,)})
    TransactionValidator.validate_transfer("1234567812345678", "0000000000000000", 500, db)