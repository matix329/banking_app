# Changelog

## [1.0.0] - 2024-11-10
### Added
- Initial structure and organization of the project with modular separation of concerns.
- **DatabaseManager** (`db_manager.py`): Handles SQLite database setup, connections, and queries.
- **AccountManager** (`account_manager.py`): Manages account operations such as creating accounts, adding income, transferring funds, and closing accounts.
- **Validator** (`validator.py`): Implements the Luhn algorithm to validate card numbers.
- **Constants** (`constants.py`): Stores reusable constants.
- **Main Entry Point** (`main.py`): Provides a command-line interface for users to interact with the banking system.
- **Tests**: Unit tests for `AccountManager`, `DatabaseManager`, and `Validator` modules, covering functionality like account creation, balance updates, transfers, and validation.

## [1.1.0] - 2024-11-11
### Added
- **Transaction History**: View a log of past transactions (income and transfers) for each account.
- **`transactions` table**: A new table in the database to store the transaction history for each account, with fields `account_number`, `transaction_type`, `amount`, and `date`.
- **`record_transaction` function** in `AccountManager`: This function automatically records transactions (`add income` and `transfer`) in the `transactions` table.
- **`get_transaction_history` function** in `AccountManager`: A function that allows users to view the transaction history for a given account.

### Changed
- **Transfer handling**: Each `add income` and `transfer` operation is now logged in the `transactions` table to ensure a complete transaction history.

## [1.1.1] - 2024-11-12
### Fixed
- Added error handling for database connection and queries to prevent crashes when the database is unavailable.
- Improved database query execution with better error messages when the connection is not available.

## [1.1.2] - 2024-11-13
### Added
- Improved `close_account` method to ensure better validation and error handling.

## [1.2.2] - 2024-11-14
### Added
- **Daily transaction limit functionality**:
  - Introduced a new table `daily_limits` to store daily transaction limits for users.
  - Added functionality to set and update daily limits for users.
  - Implemented validation to ensure users can only change their daily limit up to 3 times a day.
  - Added support for checking daily limits during transactions, preventing transfers that exceed the set limit.

### Changed
- **Transfer functionality**:
  - Updated `transfer` method to check the daily limit before processing a transaction. If the transaction exceeds the limit, it is denied.
  
### Fixed
- Resolved issues with limit changes, ensuring that users can change their daily limit only up to 3 times per day.
  
### Database Changes
- Added a new table `daily_limits` to track the daily limit, set date, and number of changes for each account.

## [1.2.3] - 2024-11-15
### Added
- Test functions for database, transfers, and daily limit functionality

## [v1.2.4] - 2024-11-16
### Added
- Implemented account locking after 3 consecutive failed login attempts.
- Added `failed_attempts` and `locked` columns in the `card` table to track and manage failed login attempts.

### Changed
- Modified account login logic to lock the account after 3 failed login attempts and raise an error when the account is locked.

### Fixed
- Fixed issues with account lock logic that caused errors in the login flow.