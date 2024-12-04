from argon2 import PasswordHasher

class Hasher:
    @staticmethod
    def hash(pin: str) -> str:
        ph = PasswordHasher()
        return ph.hash(pin)

    @staticmethod
    def check(stored_hash: str, entered_pin: str) -> bool:
        ph = PasswordHasher()
        try:
            return ph.verify(stored_hash, entered_pin)
        except Exception:
            return False