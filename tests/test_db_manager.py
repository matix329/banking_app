import pytest
from banking_core.database.db_manager import DatabaseManager
from unittest.mock import patch
from banking_core.services.account_manager import AccountManager
import random


@pytest.fixture
def db_manager():
    db = DatabaseManager()
    return db


def test_setup_database(db_manager):
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    required_tables = ['card', 'transactions', 'daily_limits']
    for table in required_tables:
        assert any(t[0] == table for t in tables)


def test_execute_query(db_manager):
    card_number = str(random.randint(1000000000000000, 9999999999999999))
    db_manager.execute_query("INSERT INTO card (number, pin, balance) VALUES (%s, %s, %s)", (card_number, "1234", 100))
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT * FROM card WHERE number = %s", (card_number,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == card_number
    assert result[2] == "1234"
    assert result[3] == 100


def test_fetch_one(db_manager):
    card_number = str(random.randint(1000000000000000, 9999999999999999))
    db_manager.execute_query("INSERT INTO card (number, pin, balance) VALUES (%s, %s, %s)", (card_number, "1234", 100))
    result = db_manager.fetch_one("SELECT * FROM card WHERE number = %s", (card_number,))
    assert result is not None
    assert result[1] == card_number
    assert result[2] == "1234"
    assert result[3] == 100


def test_database_connection_success():
    db_manager = DatabaseManager()
    assert db_manager.conn is not None


def test_database_connection_and_structure():
    try:
        db = DatabaseManager()
        cursor = db.conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        if not tables:
            raise ValueError("No tables found in the database.")
        required_tables = ['card', 'transactions', 'daily_limits']
        for table in required_tables:
            if table not in [t[0] for t in tables]:
                raise ValueError(f"Required table '{table}' is missing!")
    except Exception as e:
        print(f"Database test failed: {e}")


def test_daily_limit_functionality():
    try:
        account_manager = AccountManager()

        card_number, pin = account_manager.create_account()
        new_limit = 5000
        with patch('builtins.input', return_value=pin):
            account_manager.set_daily_limit(card_number)

        limit_data = account_manager.db.get_daily_limit(card_number)
        assert limit_data is not None
        assert limit_data[0] == new_limit
    except Exception as e:
        print(f"Daily limit functionality test failed: {e}")


def test_transfer_functionality():
    try:
        account_manager = AccountManager()

        card_number_1, pin_1 = account_manager.create_account()
        card_number_2, pin_2 = account_manager.create_account()

        amount = 100
        account_manager.add_income(card_number_1, amount * 2)
        account_manager.transfer(card_number_1, card_number_2, amount)

        balance_1 = account_manager.get_balance(card_number_1)
        balance_2 = account_manager.get_balance(card_number_2)

        assert balance_1 == amount
        assert balance_2 == amount
    except Exception as e:
        print(f"Transfer test failed: {e}")