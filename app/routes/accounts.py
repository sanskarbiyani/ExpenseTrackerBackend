from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.dependencies.shared import get_db
from app.schemas.accounts import AccountBase, CreateAccountResponse
from app.schemas.base_response import APIResponse
from app.dependencies.auth import get_current_user
from app.services.account_service import create_new_account, get_all_accounts_by_user_id

router = APIRouter()

@router.get("", response_model=APIResponse, tags=["accounts"])
async def get_all_accounts(user_id = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Endpoint to retrieve all accounts.
    """
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User ID is required to access accounts."
        )
    all_accounts = await get_all_accounts_by_user_id(user_id=user_id, db=db)
    accounts = [CreateAccountResponse.model_validate(account) for account in all_accounts]
    return APIResponse(success=True, data=accounts)

@router.post("/create", response_model=APIResponse, tags=["accounts"])
async def create_account(request: AccountBase, user_id = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Endpoint to create a new account.
    """
    if not request.name:
        return APIResponse(success=False, error="Account name is required.")
    if request.balance < 0:
        return APIResponse(success=False, error="Balance cannot be negative.")
    if not user_id:
        return HTTPException(
            status_code=401,
            detail="Unauthorized: User ID is required to create an account."
        )
    
    new_account = await create_new_account(account=request, user_id=user_id, db=db)
    account = CreateAccountResponse.model_validate(new_account)
    
    return APIResponse(success=True, data=account)

# test push