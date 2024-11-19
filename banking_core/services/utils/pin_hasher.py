import bcrypt
import binascii

class PinHasher:
    @staticmethod
    def hash_pin(pin: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pin.encode('utf-8'), salt)
        return hashed

    @staticmethod
    def check_pin(stored_hash: bytes, entered_pin: str) -> bool:
        try:
            if isinstance(stored_hash, str):
                stored_hash = binascii.unhexlify(stored_hash[2:])

            return bcrypt.checkpw(entered_pin.encode('utf-8'), stored_hash)
        except ValueError as e:
            print(f"Error during password check: {e}")
            raise