from pydantic import BaseModel, EmailStr, model_validator, validate_email
from app.models.users import User
from app.schemas.users import UserBase

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str 
    password: str

    # Use Below modelt to add Validation for username or email
    # @model_validator(mode="before")
    # @classmethod
    # def check_username_or_email(cls, values):
        # username = values.get("username")
        # email = values.get("email")
        # if not username and email:
        #     raise ValueError("Either username or email must be provided.")
    
        # if email:
        #     try:
        #         validate_email(email)
        #     except ValueError:
        #         raise ValueError("Invalid email format")

        # return values

class TokenResponse(BaseModel):
    access_token: str = ""
    token_type: str = ""
    user: UserBase | None = None