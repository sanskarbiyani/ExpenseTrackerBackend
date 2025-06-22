import os
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

from app.auth.jwt import verify_access_token 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY");
ALGORITHM = os.getenv("ALGORITHM")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Default to 30 minutes if not set

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = verify_access_token(token)  # Reuse your existing function

    # Ensure 'sub' exists in the payload
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing 'sub' in token")

    return user_id