from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logging import log_to_db

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

def verify_password(plain_password: str, hashed_password: str, user_id: int) -> bool:
    """Verify a plain password against a hashed password."""
    try:
        return pwd_hasher.verify(hashed_password, plain_password)
    except InvalidHashError:
        try:
            # If bcrypt fails, try with passlib
            _ = asyncio.create_task(log_to_db(error_message="Argon verification failed, trying with bcryt", level="Info", method="verify_password", user_id=user_id, action="Argon password_verification"))
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # If both fail, return False
            return False
    except VerifyMismatchError:
        print("Password mismatch error during verification.")
        return False