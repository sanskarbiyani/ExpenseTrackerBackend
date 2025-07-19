from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.dependencies.shared import get_db
from app.schemas.auth import LoginRequest, TokenResponse, TokenRequest
from app.schemas.base_response import APIResponse
from app.services.auth_service import verfy_user_credentials
from app.services.user_services import get_user
from app.auth.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.schemas.users import UserBase

router = APIRouter()


@router.post("/login", response_model= APIResponse, tags=["auth"])
async def login_user(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Endpoint to login a user and return a token."""
    user = await verfy_user_credentials(request, db)
    if user:
        # Here you would typically generate a JWT token or similar
        access_token, refresh_token = await asyncio.gather(
            create_access_token(data={"sub": user.id}),
            create_refresh_token(data={"sub": user.id})
        )
        token_response = TokenResponse(access_token=access_token, token_type="bearer", refresh_token=refresh_token, user=UserBase.model_validate(user))
        return APIResponse(data=token_response)

@router.post("/validate", response_model=APIResponse, tags=["auth"])
async def validate_token(request: TokenRequest, db: AsyncSession = Depends(get_db)):
    """Endpoint to validate a token."""
    if not request.token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    payload = await verify_refresh_token(request.token)
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    access_token, refresh_token = await asyncio.gather(
            create_access_token(data={"sub": user_id}),
            create_refresh_token(data={"sub": user_id})
        )
    current_user = await get_user(user_id, db)
    token_response = TokenResponse(access_token=access_token, token_type="bearer", refresh_token=refresh_token, user=UserBase.model_validate(current_user))
    return APIResponse(data=token_response)
    
