from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.shared import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.base_response import APIResponse
from app.services.auth_service import verfy_user_credentials
from app.auth.jwt import create_access_token
from app.schemas.users import UserBase

router = APIRouter()


@router.post("/login", response_model= APIResponse, tags=["auth"])
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint to login a user and return a token."""
    user = verfy_user_credentials(request, db)
    if user:
        # Here you would typically generate a JWT token or similar
        token = create_access_token(data={"sub": user.id})
        token_response = TokenResponse(access_token=token, token_type="bearer", user=UserBase.model_validate(user))
        return APIResponse(data=token_response)
