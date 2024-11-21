import pytest
import psycopg2
from unittest import mock
from unittest.mock import MagicMock
from banking_core.database import DatabaseConnection

@pytest.fixture(autouse=True)
def mock_env_variables():
    with mock.patch.dict('os.environ', {
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "test_host",
        "DB_PORT": "5432"
    }):
        yield

def test_connection():
    with mock.patch('psycopg2.connect') as mocked_connect:
        mocked_connect.return_value = MagicMock(spec=psycopg2.extensions.connection)
        DatabaseConnection()
        mocked_connect.assert_called_with(
            dbname="test_db",
            user="test_user",
            password="test_password",
            host="test_host",
            port="5432"
        )

def test_failed_connection():
    with mock.patch('psycopg2.connect') as mocked_connect:
        mocked_connect.side_effect = psycopg2.Error
        with pytest.raises(Exception) as e_info:
            DatabaseConnection()
        assert "Database connection error: " in str(e_info.value)

def test_get_connection():
    with mock.patch('psycopg2.connect') as mocked_connect:
        mocked_connect.return_value = "mocked_connection"
        db = DatabaseConnection()
        assert db.get_connection() == "mocked_connection"

def test_connection_closes():
    with mock.patch('psycopg2.connect') as mocked_connect:
        mocked_close = MagicMock()
        mocked_connect.return_value.close = mocked_close
        db = DatabaseConnection()
        db.close()
        mocked_close.assert_called_once()

def test_failed_close():
    with mock.patch('psycopg2.connect') as mocked_connect:
        mocked_close = MagicMock()
        mocked_close.side_effect = psycopg2.Error("Error closing the database connection")
        mocked_connect.return_value.close = mocked_close
        db = DatabaseConnection()
        with pytest.raises(Exception) as close_info:
            db.close()
        assert "Error closing the database connection" in str(close_info.value)