from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.shared import get_db
from app.schemas.accounts import AccountBase
from app.schemas.base_response import APIResponse
from app.dependencies.auth import get_current_user
from app.services.account_service import create_new_account

router = APIRouter()

@router.get("", response_model=APIResponse, tags=["accounts"])
def get_all_accounts(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all accounts.
    This is a placeholder function and should be implemented.
    """
    # Placeholder for actual implementation
    return {"message": "This endpoint will return all accounts."}

@router.post("/create", response_model=APIResponse, tags=["accounts"])
def create_account(request: AccountBase, user_id = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Endpoint to create a new account.
    This is a placeholder function and should be implemented.
    """
    # Placeholder for actual implementation
    if not request.name:
        return APIResponse(success=False, error="Account name is required.")
    if request.balance < 0:
        return APIResponse(success=False, error="Balance cannot be negative.")
    
    new_account = create_new_account(account=request, user_id=user_id.id, db=db)
    
    return APIResponse(success=True, data=new_account)