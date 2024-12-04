import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from banking_core.services.limits.limit_manager import LimitManager

@pytest.fixture
def db_mock():
    mock = MagicMock()
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = ('1234',)
    mock.conn.cursor.return_value = cursor_mock
    return mock

@pytest.fixture
def limit_manager(db_mock):
    return LimitManager(db_mock)

def test_set_daily_limit_valid_pin(db_mock, limit_manager):
    db_mock.get_daily_limit.return_value = None

    with patch('builtins.input', side_effect=['1234', '2000']), \
         patch('banking_core.services.Hasher.check_pin', return_value=True) as check_pin_mock:

        limit_manager.set_daily_limit('123456')

        check_pin_mock.assert_called_once_with('1234', '1234')
        db_mock.add_daily_limit.assert_called_once_with('123456', 2000)


def test_set_daily_limit_invalid_pin(db_mock, limit_manager, capsys):
    db_mock.get_daily_limit.return_value = (1000, 1, str(datetime.now().date()))

    with patch('builtins.input', side_effect=['1234']), \
         patch('banking_core.services.Hasher.check_pin', return_value=False) as check_pin_mock:

        limit_manager.set_daily_limit('123456')

        check_pin_mock.assert_called_once_with('1234', '1234')
        captured = capsys.readouterr()
        assert 'Invalid PIN.\n' in captured.out

def test_get_stored_pin_found(limit_manager):
    assert limit_manager.get_stored_pin('123456') == '1234'

def test_get_stored_pin_not_found(limit_manager):
    cursor_mock = limit_manager.db.conn.cursor()
    cursor_mock.fetchone.return_value = None
    with pytest.raises(ValueError):
        limit_manager.get_stored_pin('123456')

def test_get_new_limit_valid():
    with patch('builtins.input', side_effect=['2000']):
        assert LimitManager(None).get_new_limit() == 2000

def test_get_new_limit_invalid(capsys):
    with patch('builtins.input', side_effect=['abc', '2000']):
        assert LimitManager(None).get_new_limit() == 2000
    captured = capsys.readouterr()
    assert captured.out == 'Invalid input: invalid literal for int() with base 10: \'abc\'. Please try again.\n'

def test_update_or_add_limit_exists(limit_manager):
    limit_data = (2000, 2, str(datetime.now().date()))
    new_limit = 3000
    limit_manager.update_or_add_limit('123456', new_limit, limit_data)
    limit_manager.db.update_daily_limit.assert_called_once_with('123456', 3000)
    limit_manager.db.add_daily_limit.assert_not_called()

def test_update_or_add_limit_doesnt_exists(limit_manager):
    new_limit = 3000
    limit_manager.update_or_add_limit('123456', new_limit, None)
    limit_manager.db.add_daily_limit.assert_called_once_with('123456', 3000)
    limit_manager.db.update_daily_limit.assert_not_called()