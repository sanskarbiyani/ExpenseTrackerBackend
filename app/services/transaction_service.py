import psycopg2
import re
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.transactions import TransactionBase, CreateTransactionResponse
from app.models.transactions import Transaction

def get_all_transactions(user_id: int, db: Session) -> list[CreateTransactionResponse]:
    """ Retrieves all transactions for a given user."""
    try:
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        return [CreateTransactionResponse.model_validate(transaction, from_attributes=True) for transaction in transactions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving transactions."
        )

def add_transaction(transaction: TransactionBase, user_id: int, db: Session) -> bool:
    """ Adds a transaction to the database."""
    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        user_id=user_id,
        # currency=transaction.currency,  # Uncomment if currency is part of the model
    )
    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
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
            detail="An unexpected error occurred while creating the transaction."
        )
    return True