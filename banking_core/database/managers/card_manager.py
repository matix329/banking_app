from ..database.base_manager import BaseManager

class CardManager(BaseManager):
    def lock_account(self, account_id):
        if not account_id:
            raise ValueError("Invalid account ID")
        self.execute_query('''UPDATE account SET locked = TRUE WHERE id = %s''', (account_id,))

    def unlock_account(self, account_id):
        if not account_id:
            raise ValueError("Invalid account ID")
        self.execute_query('''UPDATE account SET locked = FALSE, failed_attempts = 0 WHERE number = %s''', (account_id,))