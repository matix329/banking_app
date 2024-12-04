class LimitValidator:
    @staticmethod
    def validate_limit_amount(limit):
        if not isinstance(limit, (int, float)) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

    @staticmethod
    def validate_limit_change_attempts(changes_today, max_changes):
        if not isinstance(changes_today, int) or changes_today < 0:
            raise ValueError("Invalid changes_today value.")
        if changes_today >= max_changes:
            raise ValueError("Daily limit change attempts exceeded.")

    @staticmethod
    def validate_daily_limit(set_date, changes_today):
        from datetime import datetime

        if set_date != datetime.now().date():
            raise ValueError("The limit set date is not today.")
        elif changes_today >= 3:
            raise ValueError("You have reached the maximum number of changes for today.")