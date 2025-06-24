from pydantic import BaseModel, model_validator

from app.models.transactions import TransactionType

class TransactionBase(BaseModel):
    amount: float
    # currency: str
    description: str
    title: str
    transaction_type: TransactionType
    
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
        if not values.title:
            raise ValueError("Title cannot be empty.")
        if not values.transaction_type:
            raise ValueError("Transaction type must be specified.")
        if values.transaction_type not in TransactionType:
            raise ValueError("Invalid transaction type. Must be 'income' or 'expense'.")
        return values
        

class CreateTransactionResponse(TransactionBase):
    id: int

    model_config = {
        "from_attributes": True,
    }