import asyncio
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.shared import get_db
from app.dependencies.auth import get_current_user
from app.schemas.base_response import APIResponse
from app.schemas.transactions import TransactionBase, CreateTransactionResponse, FilterTransaction
from app.services.transaction_service import add_transaction, get_all_transactions, get_balance_summary_details, get_monthly_balance_summary

router = APIRouter()

@router.get("", response_model=APIResponse, tags=["transactions"])
async def get_transactions(transaction_filters: FilterTransaction = Depends(), db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Endpoint to retrieve all transactions for the current user."""
    user_transactions = await get_all_transactions(user_id, transaction_filters, db)
    return APIResponse(data=user_transactions)

@router.post("/create", response_model= APIResponse, tags=["transactions"])
async def create_transaction(request: TransactionBase, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Endpoint to create a new transaction."""
    new_transaction = await add_transaction(request, user_id, db)
    if not new_transaction:
        return APIResponse(success=False, error="Failed to create transaction.")
    return APIResponse(data={"message": "Transaction created successfully.", "id": new_transaction.id})

@router.get("/balance-summary", response_model=APIResponse, tags=["transactions"])
async def get_balance_summary(account_id = Query(None), db1: AsyncSession = Depends(get_db, use_cache=False), db2: AsyncSession = Depends(get_db, use_cache=False), user_id: int = Depends(get_current_user)):
    """Endpoint to get the balance summary for the current user."""
    balance_summary, monthly_balance_summary = await asyncio.gather(
        get_balance_summary_details(user_id, account_id, db1),
        get_monthly_balance_summary(user_id, account_id, db2)
    )
    if not balance_summary and not monthly_balance_summary:
        return APIResponse(success=False, error="No transactions found.")
    combined_data = {
        "balance_summary": balance_summary,
        "monthly_balance_summary": monthly_balance_summary
    }
    return APIResponse(data=combined_data)

