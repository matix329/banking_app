import pytest
from unittest.mock import MagicMock
from datetime import datetime
from banking_core.database import BaseManager, DailyLimitManager

db_mock = MagicMock(BaseManager)
manager = DailyLimitManager(db_mock)

def test_get_daily_limit():
    account_number = '12345'
    expected_result = ('1000', 200, '2024-11-20')
    db_mock.fetch_one.return_value = expected_result

    result = manager.get_daily_limit(account_number)

    db_mock.fetch_one.assert_called_once_with('''SELECT daily_limit, changes_today, set_date 
                                    FROM daily_limits WHERE account_number = %s ORDER BY set_date DESC LIMIT 1''', (account_number,))
    assert result == expected_result

def test_add_daily_limit():
    account_number = '12345'
    daily_limit = 1500
    current_date = datetime.now().date()

    manager.add_daily_limit(account_number, daily_limit)

    db_mock.execute_query.assert_called_once_with('''INSERT INTO daily_limits (account_number, daily_limit, set_date, changes_today)
                                 VALUES (%s, %s, %s, %s)''', (account_number, daily_limit, str(current_date), 0))

def test_update_daily_limit():
    db_mock.reset_mock()

    account_number = '12345'
    new_limit = 2000
    current_date = datetime.now().date()

    manager.update_daily_limit(account_number, new_limit)

    db_mock.execute_query.assert_called_once_with('''UPDATE daily_limits
                                 SET daily_limit = %s, set_date = %s, changes_today = changes_today + 1
                                 WHERE account_number = %s AND set_date = %s''', (new_limit, str(current_date), account_number, str(current_date)))

def test_get_daily_limit_no_result():
    account_number = '12345'
    db_mock.fetch_one.return_value = None

    result = manager.get_daily_limit(account_number)

    db_mock.fetch_one.assert_called_once_with('''SELECT daily_limit, changes_today, set_date 
                                    FROM daily_limits WHERE account_number = %s ORDER BY set_date DESC LIMIT 1''', (account_number,))
    assert result is None
