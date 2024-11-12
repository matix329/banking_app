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

def test_database_connection_failure():
    with pytest.raises(Exception) as exc_info:
        db_manager = DatabaseManager("non_existent_db.s3db")
    assert "Database connection error" in str(exc_info.value)