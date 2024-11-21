import pytest
from banking_core.services.transactions.transaction_manager import TransactionManager

class MockDb:
    def __init__(self):
        self.queries = []
        self.conn = self
        self.transactions = []

    def execute_query(self, query, params):
        self.queries.append((query, params))
        if "INSERT INTO transactions" in query:
            self.transactions.append(params)

    def cursor(self):
        return self

    def fetchall(self):
        return self.transactions

    def execute(self, query, params):
        self.queries.append((query, params))

    def fetch_one(self, query, params):
        self.queries.append((query, params))
        if "SELECT * FROM card WHERE number = %s" in query:
            if params[0] == "2222222222222222":
                return {"number": params[0]}
            return None
        if "SELECT balance FROM card WHERE number = %s" in query:
            if params[0] == "1111":
                return (200,)
        return None

@pytest.fixture
def db():
    return MockDb()

@pytest.fixture
def transaction_manager(db):
    return TransactionManager(db)

def test_transfer(transaction_manager, db):
    transaction_manager.transfer("1111", "2222222222222222", 100)

    assert ("UPDATE card SET balance = balance - %s WHERE number = %s", (100, "1111")) in db.queries
    assert ("UPDATE card SET balance = balance + %s WHERE number = %s", (100, "2222222222222222")) in db.queries

    assert ("1111", "transfer_out", -100) in db.transactions
    assert ("2222222222222222", "transfer_in", 100) in db.transactions

def test_add_income(transaction_manager, db):
    transaction_manager.add_income("1111", 100)
    assert ("UPDATE card SET balance = balance + %s WHERE number = %s", (100, "1111")) in db.queries

def test_add_invalid_income_throws_exception(transaction_manager):
    with pytest.raises(ValueError):
        transaction_manager.add_income("1111", -1)

def test_get_transaction_history(transaction_manager, db):
    transaction_manager.get_transaction_history("1111")
    assert ("SELECT date, transaction_type, amount FROM transactions WHERE account_number = %s ORDER BY date DESC", ("1111", )) in db.queries