from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
import traceback

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_hasher = PasswordHasher(
    time_cost=2,       # Number of iterations (lower = faster)
    memory_cost=2**14, # 16 MB RAM usage (reasonable for free tier)
    parallelism=2,     # Number of threads (adjust to 1 if CPU is too constrained)
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    result = False
    try:
        result = pwd_hasher.verify(hashed_password, plain_password)
    except InvalidHashError as e:
        traceback.print_exc()
        print(f"Invalid hash error: {e}")
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