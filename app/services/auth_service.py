from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.auth import LoginRequest
from app.models.users import User
from app.utils.security import hash_password, verify_password


def verfy_user_credentials(request: LoginRequest, db: Session) -> User:
    """Verify user credentials and return the user object."""
    hashed_password = hash_password(request.password)

    try:
        if not request.username:
            user = db.query(User).filter_by(email = request.email, password=hashed_password).first()
        else:
            user = db.query(User).filter_by(username=request.username).first()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while verifying user credentials."
        )

    if not user or not bool(user.is_active):
        raise HTTPException(
            status_code=401,
            detail="User not found."
        )
    
    # Verify the password
    if user and not verify_password(request.password, str(user.password)):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password."
        )
    return user