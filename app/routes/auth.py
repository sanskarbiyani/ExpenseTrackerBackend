from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.shared import get_db
from app.schemas.auth import LoginRequest, TokenResponse, TokenRequest
from app.schemas.base_response import APIResponse
from app.services.auth_service import verfy_user_credentials
from app.auth.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.schemas.users import UserBase

router = APIRouter()


@router.post("/login", response_model= APIResponse, tags=["auth"])
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint to login a user and return a token."""
    user = verfy_user_credentials(request, db)
    if user:
        # Here you would typically generate a JWT token or similar
        token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        token_response = TokenResponse(access_token=token, token_type="bearer", refresh_token=refresh_token, user=UserBase.model_validate(user))
        return APIResponse(data=token_response)

@router.post("/validate", response_model=APIResponse, tags=["auth"])
def validate_token(request: TokenRequest, db: Session = Depends(get_db)):
    """Endpoint to validate a token."""
    if not request.token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    payload = verify_refresh_token(request.token)
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})
    token_response = TokenResponse(access_token=token, token_type="bearer", refresh_token=refresh_token)
    return APIResponse(data=token_response)
    
