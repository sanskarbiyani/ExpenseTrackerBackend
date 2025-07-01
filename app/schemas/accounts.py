from pydantic import BaseModel

class AccountBase(BaseModel):
    name: str
    description: str | None = None
    balance: float = 0.0

class CreateAccountResponse(AccountBase):
    id: int

    model_config = {
        "from_attributes": True,
    }