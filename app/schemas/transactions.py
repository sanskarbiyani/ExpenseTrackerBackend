from pydantic import BaseModel, model_validator

class TransactionBase(BaseModel):
    amount: float
    # currency: str
    description: str
    
    model_config = {
        "from_attributes": True,
    }

    @model_validator(mode="before")
    @classmethod
    def check_amount(cls, values):
        amount = values.amount
        desc = values.description
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not desc:
            raise ValueError("Description cannot be empty.")
        return values
        

class CreateTransactionResponse(TransactionBase):
    id: int

    model_config = {
        "from_attributes": True,
    }