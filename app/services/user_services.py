import re
import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.users import User
from app.schemas.users import UserCreate
from app.utils.security import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database."""
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, psycopg2.errors.UniqueViolation):
            # Handle unique constraint violation
            constraint_name = e.orig.diag.constraint_name
            message = str(e.orig.diag.message_detail)
            match = re.search(r"\((\w+)\)=\((.+?)\)", message)
            if match:
                field, value = match.groups()
                raise HTTPException(
                    status_code=400,
                    detail=f"{field.capitalize()} '{value}' already exists."
                )
            else:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail= f"{constraint_name} already exists."
                )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user."
        )
    return new_user