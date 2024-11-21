import pytest
import psycopg2
from banking_core.database import setup

def patch_execute(query, vars=None):
    return None

def patch_commit():
    return None

@pytest.fixture
def connect_db(mocker):
    conn = mocker.Mock()
    cursor = mocker.Mock()
    cursor.execute = mocker.Mock(side_effect=patch_execute)
    conn.commit = mocker.Mock(side_effect=patch_commit)
    conn.cursor.return_value = cursor
    mocker.patch.object(psycopg2, 'connect', return_value=conn)
    return conn

def test_setup_database(connect_db):
    setup.setup_database(connect_db)
    connect_db.cursor.return_value.execute.assert_called()
    connect_db.commit.assert_called()

def test_setup_database_error(mocker, connect_db):
    error = psycopg2.Error("Error!")
    connect_db.cursor.return_value.execute.side_effect = error
    with pytest.raises(psycopg2.Error):
        setup.setup_database(connect_db)