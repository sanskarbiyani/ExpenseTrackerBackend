from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.schemas.auth import LoginRequest
from app.models.users import User
from app.utils.security import hash_password, verify_password


async def verfy_user_credentials(request: LoginRequest, db: AsyncSession) -> User:
    """Verify user credentials and return the user object."""
    try:
        result = await db.execute(select(User).where(User.username == request.username))
        user = result.scalars().first()
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