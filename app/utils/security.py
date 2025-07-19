from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    result = False
    try:
        result = pwd_hasher.verify(plain_password, hashed_password)
    except InvalidHashError:
        try:
            # If bcrypt fails, try with passlib
            print("Bcrypt verification failed, trying passlib...")
            result = pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # If both fail, return False
            return False
    except VerifyMismatchError:
        print("Password mismatch error during verification.")
    return result