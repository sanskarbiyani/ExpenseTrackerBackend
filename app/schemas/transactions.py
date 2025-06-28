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
        amount = values.get("amount")
        desc = values.get("description")
        transaction_type = values.get("transaction_type")
        if amount is None or amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not desc:
            raise ValueError("Description cannot be empty.")
        if not transaction_type:
            raise ValueError("Transaction type must be specified.")
        if values.get("transaction_type") not in TransactionType:
            raise ValueError("Invalid transaction type. Must be 'income' or 'expense'.")
        return values
        

class CreateTransactionResponse(TransactionBase):
    id: int

    model_config = {
        "from_attributes": True,
    }