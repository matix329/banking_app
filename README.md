# Banking App

A simple banking system in Python with functionalities for creating accounts, logging in, transferring funds, and managing account balances. The application is built using SQLite for data storage and includes basic validation with the Luhn algorithm for card numbers.

## Features
- **Account Creation**: Generate a new card number and PIN for a user.
- **Login**: Authenticate users with their card number and PIN.
- **Balance Management**: Check balance, add income, and transfer funds between accounts.
- **Account Closure**: Delete an account from the database.
- **Card Number Validation**: Uses the Luhn algorithm to validate card numbers.

## Requirements
- Python 3.x
- `pytest` for running unit tests
- SQLite (bundled with Python)

## Changelog
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
- **`transactions` table**: A new table in the database to store the transaction history for each account, with fields `account_number`, `transaction_type`, `amount`, and `date`.
- **`record_transaction` function** in `AccountManager`: This function automatically records transactions (`add income` and `transfer`) in the `transactions` table.
- **`get_transaction_history` function** in `AccountManager`: A function that allows users to view the transaction history for a given account.

### Changed
- **Transfer handling**: Each `add income` and `transfer` operation is now logged in the `transactions` table to ensure a complete transaction history.