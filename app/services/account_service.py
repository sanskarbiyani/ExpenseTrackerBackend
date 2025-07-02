import re
from fastapi import HTTPException, status
import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.accounts import AccountBase
from app.models.accounts import Account

def create_new_account(account: AccountBase, user_id: int, db: Session) -> Account:
    new_account = Account(
        user_id=user_id,
        name=account.name,
        description=account.description,
        balance=account.balance
    )
    try:
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
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
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail= f"Somethign went wrong while creating the account."
                )
    return new_account


def get_all_accounts_by_user_id(user_id, db: Session) -> list[Account]:
    accounts = db.query(Account).filter(Account.user_id == user_id).order_by(Account.updated_at.desc()).all()
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No accounts found for the user."
        )
    return accounts