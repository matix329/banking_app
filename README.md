# Banking app
Modular banking system in Python with SQLite, supporting accounts, login, and transfers

---

## Changelog

### [1.0] - 2024-11-08

#### Added
- Initial project structure with two main directories: `banking_core` for core application logic and `tests` for unit tests.

### [1.0.1] - 2024-11-09

#### Added
- `validator.py` in the `services` directory – a new module containing functions related to the Luhn algorithm (`luhn_checksum` and `is_valid_card_number`).
- `test_validator.py` in the `tests` directory – new unit tests for the `luhn_checksum` and `is_valid_card_number` functions.

### [1.0.2] - 2024-11-09

#### Added
- `requirements.txt` – added to list the project dependencies.

#### Changed
- Updated `test_validator.py` to validate a different card number that satisfies the Luhn algorithm.
