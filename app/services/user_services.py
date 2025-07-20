import re
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.users import User
from app.schemas.users import UserCreate
from app.utils.security import hash_password

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Create a new user in the database."""
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError as e:
        await db.rollback()
        error_message = str(e.orig)
        print(f"IntegrityError: {e.orig.__class__.__name__}")
        match = re.search(r'Key \((\w+)\)=\((.+?)\)', error_message)
        if match:
            field, value = match.groups()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.capitalize()} '{value}' already exists."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity check failed."
            )
    except Exception as e:
        print(f"Unexpected error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user."
        )
    return new_user

async def get_user(user_id: int, db: AsyncSession) -> User:
    """Retrieve a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user