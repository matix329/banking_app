class LimitValidator:
    @staticmethod
    def validate_limit_amount(limit):
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

    @staticmethod
    def validate_limit_change_attempts(changes_today, max_changes):
        if changes_today >= max_changes:
            raise ValueError("Daily limit change attempts exceeded.")