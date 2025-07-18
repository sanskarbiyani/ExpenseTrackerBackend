import psycopg2
import re
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.transactions import TransactionBase, CreateTransactionResponse, FilterTransaction
from app.models.transactions import Transaction
from app.schemas.balance_summary import BalanceSummary

async def get_all_transactions(user_id: int, transaction_filters: FilterTransaction, db: AsyncSession) -> list[CreateTransactionResponse]:
    """ Retrieves all transactions for a given user."""
    try:
        stmt = select(Transaction).where(Transaction.user_id == user_id)
        if transaction_filters.account_id:
            transactions = stmt.filter(Transaction.account_id == transaction_filters.account_id)
        if transaction_filters.transaction_type:
            transactions = stmt.filter(Transaction.transaction_type == transaction_filters.transaction_type)
        if transaction_filters.start_date:
            transactions = stmt.filter(Transaction.created_at >= transaction_filters.start_date)
        if transaction_filters.end_date:
            transactions = stmt.filter(Transaction.created_at <= transaction_filters.end_date)
        
        stmt = stmt.order_by(Transaction.created_at.desc()).limit(20)
        result = await db.execute(stmt)
        transactions = result.scalars().all()

        return [CreateTransactionResponse.model_validate(transaction, from_attributes=True) for transaction in transactions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving transactions."
        )

async def add_transaction(transaction: TransactionBase, user_id: int, db: AsyncSession):
    """ Adds a transaction to the database."""
    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        user_id=user_id,
        transaction_type=transaction.transaction_type,
        account_id=transaction.account_id, 
        # currency=transaction.currency,  # Uncomment if currency is part of the model
    )
    try:
        db.add(new_transaction)
        await db.commit()
        await db.refresh(new_transaction)
    except IntegrityError as e:
        await db.rollback()
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
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the transaction."
        )
    if new_transaction.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transaction creation failed, ID is None."
        )
    return new_transaction

async def get_balance_summary_details(user_id: int, account_id: int, db: AsyncSession) -> BalanceSummary:
    """ Retrieves the balance summary - today, week and month balance for a given user."""
    try:
        sql = text("""
            SELECT * from get_balance_summary(:user_id, :account_id)
        """)
        result = await db.execute(sql, {"user_id": user_id, "account_id": account_id})
        balance_summary = result.fetchone()
        if not balance_summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No balance summary found for the given user and account."
            )
        return BalanceSummary.model_validate(balance_summary, from_attributes=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the balance summary."
        )