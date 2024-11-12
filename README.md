# Banking App

A simple banking system in Python with functionalities for creating accounts, logging in, transferring funds, and managing account balances. The application is built using SQLite for data storage and includes basic validation with the Luhn algorithm for card numbers.

## Features
- **Account Creation**: Generate a new card number and PIN for a user.
- **Login**: Authenticate users with their card number and PIN.
- **Balance Management**: Check balance, add income, and transfer funds between accounts.
- **Account Closure**: Delete an account from the database.
- **Card Number Validation**: Uses the Luhn algorithm to validate card numbers.
- **Transaction history**: View a log of past transactions

## Version
Current version: 1.1.1

## Requirements
- Python 3.x
- `pytest` for running unit tests
- SQLite (bundled with Python)

## Changelog
For detailed information on updates and changes, see the [CHANGELOG.md](CHANGELOG.md).