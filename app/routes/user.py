from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.shared import get_db
from app.services.user_services import create_user
from app.auth.jwt import create_access_token
from app.schemas.users import UserBase, UserCreate 
from app.schemas.auth import TokenResponse

router = APIRouter()

@router.post("/register", response_model=TokenResponse, tags=["users"])
def register_user(request: UserCreate ,db: Session = Depends(get_db)):
    """Register a new user and return a token response."""
    user = create_user(db, request)
    token = create_access_token(data={"sub": user.id})
    return TokenResponse(access_token=token, token_type="bearer", user=UserBase.model_validate(user))