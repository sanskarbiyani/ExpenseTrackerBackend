from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.shared import get_db
from app.schemas.base_response import APIResponse
from app.services.user_services import create_user
from app.auth.jwt import create_access_token
from app.schemas.users import UserBase, UserCreate 
from app.schemas.auth import TokenResponse

router = APIRouter()

@router.post("/register", response_model=APIResponse, tags=["users"])
async def register_user(request: UserCreate ,db: AsyncSession = Depends(get_db)):
    """Register a new user and return a token response."""
    user = await create_user(db, request)
    token = await create_access_token(data={"sub": user.id})
    tokenResponse = TokenResponse(access_token=token, token_type="bearer", user=UserBase.model_validate(user))
    return APIResponse(data=tokenResponse)