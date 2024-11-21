import pytest
import psycopg2
from dotenv import load_dotenv
import os
from banking_core.database.base_manager import BaseManager

load_dotenv()

TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")

@pytest.fixture
def base_manager():
    conn = psycopg2.connect(
        dbname=TEST_DB_NAME,
        user=TEST_DB_USER,
        password=TEST_DB_PASSWORD,
        host=TEST_DB_HOST,
        port=TEST_DB_PORT
    )
    base_manager = BaseManager(conn)
    yield base_manager
    conn.close()

def test_execute_query(base_manager):
    try:
        base_manager.execute_query("SELECT * FROM test_table")
    except psycopg2.Error as e:
        pytest.fail(f"Database query error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
    assert True

def test_fetch_one(base_manager):
    try:
        result = base_manager.fetch_one("SELECT * FROM test_table LIMIT 1")
    except psycopg2.Error as e:
        pytest.fail(f"Database query error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
    assert isinstance(result, tuple)

def test_exceptions(base_manager):
    with pytest.raises(psycopg2.Error):
        base_manager.execute_query("THIS IS NOT VALID SQL")
    with pytest.raises(psycopg2.Error):
        base_manager.fetch_one("THIS IS NOT VALID SQL")