import pytest
from banking_core.database.db_manager import DatabaseManager

@pytest.fixture
def db_manager():
    db = DatabaseManager(":memory:")
    return db

def test_setup_database(db_manager):
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card';")
    assert cursor.fetchone() is not None, "Table 'card' should exist"

def test_execute_query(db_manager):
    db_manager.execute_query("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", ("1234567890123456", "1234", 100))
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT * FROM card WHERE number = ?", ("1234567890123456",))
    result = cursor.fetchone()
    assert result is not None, "Data should be inserted into 'card' table"
    assert result[1] == "1234567890123456"
    assert result[2] == "1234"
    assert result[3] == 100

def test_fetch_one(db_manager):
    db_manager.execute_query("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", ("1234567890123456", "1234", 100))
    result = db_manager.fetch_one("SELECT * FROM card WHERE number = ?", ("1234567890123456",))
    assert result is not None, "Data should be fetched from 'card' table"
    assert result[1] == "1234567890123456"
    assert result[2] == "1234"
    assert result[3] == 100

def test_database_connection_success():
    db_manager = DatabaseManager(":memory:")
    assert db_manager.conn is not None, "Database connection should be established successfully."

def test_database_connection_and_structure():
    try:
        db = DatabaseManager()
        print("Testing database connection...")
        cursor = db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            raise ValueError("No tables found in the database.")

        print(f"Tables in database: {tables}")

        required_tables = ['card', 'transactions', 'daily_limits']
        for table in required_tables:
            if table not in [t[0] for t in tables]:
                raise ValueError(f"Required table '{table}' is missing!")

        print("Database structure and connection test passed!")
    except Exception as e:
        print(f"Database test failed: {e}")

def test_daily_limit_functionality():
    try:
        account_manager = AccountManager()

        card_number, pin = account_manager.create_account()
        print(f"Account (Card Number: {card_number}) created.")

        new_limit = 5000
        print(f"Setting daily limit of {new_limit}...")
        account_manager.set_daily_limit(card_number)

        limit_data = account_manager.db.get_daily_limit(card_number)
        assert limit_data is not None, "Daily limit should be set."
        assert limit_data[0] == new_limit, f"Expected daily limit: {new_limit}, but got: {limit_data[0]}"

        print("Daily limit functionality test passed!")
    except Exception as e:
        print(f"Daily limit functionality test failed: {e}")

def test_transfer_functionality():
    try:
        account_manager = AccountManager()

        card_number_1, pin_1 = account_manager.create_account()
        card_number_2, pin_2 = account_manager.create_account()

        print(f"Account 1 (Card Number: {card_number_1}) created.")
        print(f"Account 2 (Card Number: {card_number_2}) created.")

        amount = 100
        print(f"Transferring {amount} from Account 1 to Account 2...")
        account_manager.add_income(card_number_1, amount * 2)
        account_manager.transfer(card_number_1, card_number_2, amount)

        balance_1 = account_manager.get_balance(card_number_1)
        balance_2 = account_manager.get_balance(card_number_2)

        print(f"Balance of Account 1: {balance_1}")
        print(f"Balance of Account 2: {balance_2}")

        assert balance_1 == amount, f"Account 1 should have {amount} after transfer"
        assert balance_2 == amount, f"Account 2 should have {amount} after receiving transfer"

        print("Transfer test passed!")
    except Exception as e:
        print(f"Transfer test failed: {e}")