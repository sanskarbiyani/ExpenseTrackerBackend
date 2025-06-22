
import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt
from jwt import ExpiredSignatureError, InvalidAudienceError, InvalidIssuedAtError, InvalidIssuerError, InvalidTokenError
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY");
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Default to 30 minutes if not set

def create_access_token(data: dict):
    to_encode = data.copy()

    if "sub" not in to_encode:
        raise ValueError("Token payload must include 'sub' field")
    
    # Cast to string
    to_encode["sub"] = str(to_encode["sub"])

    issued_at = datetime.now(timezone.utc)
    expire = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iss": "https://expensetrackerbackend-wtq2.onrender.com",
        "aud": "https://expensetrackerbackend-wtq2.onrender.com",
        "iat": issued_at,
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="https://expensetrackerbackend-wtq2.onrender.com",
            issuer="https://expensetrackerbackend-wtq2.onrender.com",
            options={"require": ["exp", "iss", "aud", "iat", "sub"]}
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    except InvalidIssuedAtError:
        raise HTTPException(status_code=401, detail="Invalid iat")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")