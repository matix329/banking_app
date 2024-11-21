import pytest
from banking_core.services.accounts.account_locker import AccountLocker

class MockDB:
    def __init__(self):
        self.cards = []

    def execute_query(self, query, params=None):
        card_number = params[0]
        for card in self.cards:
            if card['number'] == card_number:
                if 'failed_attempts' in query:
                    card['failed_attempts'] += 1
                elif 'locked = TRUE' in query:
                    card['locked'] = True
                elif 'locked = FALSE' in query:
                    card['locked'] = False
                    card['failed_attempts'] = 0
                return
        raise ValueError("Account not found.")
        
    def fetch_one(self, query, params=None):
        card_number = params[0]
        for card in self.cards:
            if card['number'] == card_number:
                return [card['failed_attempts'], card['locked']]
        return None

def setup_module(module):
    pytest.mock_db = MockDB()
    pytest.mock_db.cards.append({
        'number': '1111',
        'failed_attempts': 0,
        'locked': False
    })

def test_lock_account_after_failed_attempt():
    locker = AccountLocker(pytest.mock_db)

    pytest.mock_db.cards[0]['locked'] = True
    with pytest.raises(ValueError) as e_info:
        locker.lock_account_after_failed_attempt('1111')
    assert e_info.value.args[0] == "Your account is already locked."


def test_unlock_account():
    locker = AccountLocker(pytest.mock_db)

    pytest.mock_db.cards[0]['locked'] = False
    with pytest.raises(ValueError) as e_info:
        locker.unlock_account('1111')
    assert e_info.value.args[0] == "This account is not locked."