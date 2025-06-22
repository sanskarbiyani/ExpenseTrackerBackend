from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    is_active: bool = True
    credit: float = 0.0
    debit: float = 0.0

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None