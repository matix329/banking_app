Modules
=======

This section provides an overview of the core modules in the project, including their functionalities and key methods.

Core Modules
------------

Database Module
=========================================

Handles all interactions with the database, including CRUD operations for accounts and transactions.

Main Classes and Functions:
---------------------------

- **`BaseManager`**
  - Executes generic database queries:
    - `execute_query(query, params=())`: Executes an SQL query (e.g., INSERT, UPDATE).
    - `fetch_one(query, params=())`: Fetches a single record.
    - `fetch_all(query, params=())`: Fetches all matching records.

- **`CardManager`**
  - Manages account-related operations:
    - `lock_account(card_number)`: Locks an account.
    - `unlock_account(card_number)`: Unlocks an account.
    - `get_balance(card_number)`: Retrieves the account’s balance.

- **`DailyLimitManager`**
  - Handles daily transaction limits:
    - `get_daily_limit(account_number)`: Retrieves the daily limit.
    - `update_daily_limit(account_number, new_limit)`: Updates the transaction limit.

---

Accounts Module
---------------

Manages account-related operations, such as account creation, locking, and unlocking.

**Main Classes and Functions:**

- **`AccountAuthenticator`**
  - Handles login functionality:
    - `log_into_account(card_number, pin)`: Verifies login credentials and checks lock status.

- **`AccountCreator`**
  - Manages account creation:
    - `create_account()`: Generates a new account with a card number and PIN.
    - `generate_card_number()`: Uses the Luhn algorithm to generate a card number.
    - `generate_pin()`: Creates a 4-digit random PIN.

- **`AccountLocker`**
  - Manages account locking and unlocking:
    - `lock_account(card_number, pin)`: Locks an account if the PIN is correct.
    - `unlock_account(card_number)`: Unlocks an account.
    - `lock_account_after_failed_attempt(card_number)`: Locks the account after multiple failed login attempts.

---

Transactions Module
-------------------

Handles financial transactions, such as transfers and income additions.

**Main Classes and Functions:**

- **`TransactionManager`**
  - Processes financial transactions:
    - `transfer(source_card, target_card, amount)`: Transfers money between accounts.
    - `add_income(card_number, amount)`: Adds income to an account.
    - `get_transaction_history(card_number)`: Retrieves the transaction history.

- **`TransactionValidator`**
  - Validates transaction rules and sufficiency of funds:
    - `validate_transfer(source_card, target_card, amount)`: Checks if a transfer is valid.
    - `validate_amount(amount)`: Ensures the amount is positive.

---

Utils Module
------------

Provides utility functions, such as hashing PINs and validating user input.

**Main Classes and Functions:**

- **`Hasher`**
  - Handles PIN hashing and validation:
    - `hash_pin(pin)`: Hashes a plaintext PIN.
    - `check_pin(hashed_pin, entered_pin)`: Validates the entered PIN.

- **`InputValidator`**
  - Ensures user input is valid:
    - `get_positive_integer(prompt)`: Prompts the user for a positive integer.

- **`LimitValidator`**
  - Validates transaction limit changes:
    - `validate_limit_change(current_limit, new_limit)`: Ensures new limits are valid.

Limits Module
-------------

Handles validation and management of account transaction limits. This module ensures secure updates and retrieval of daily or transaction-specific limits.

**Main Classes and Functions:**

- **`LimitManager`**
  - Manages account limits and updates.
    - `get_daily_limit(account_number)`: Retrieves the daily transaction limit for a given account.
    - `set_daily_limit(account_number, new_limit)`: Updates the daily limit for the specified account.
    - `validate_limit_change(account_number, new_limit)`: Validates if a proposed new limit complies with business rules.

- **`LimitValidator`**
  - Validates transaction limits and ensures compliance.
    - `validate_transaction_limit(account_number, amount)`: Ensures the transaction is within the allowed limit.
    - `validate_daily_limit(account_number, amount)`: Checks if the transaction exceeds the daily limit.