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

    @model_validator(mode="after")
    def check_amount(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not self.description:
            raise ValueError("Description cannot be empty.")
        if not self.transaction_type:
            raise ValueError("Transaction type must be specified.")
        # By now, transaction_type is already parsed into TransactionType enum, so no need for further check
        return self
        

class CreateTransactionResponse(TransactionBase):
    id: int

    model_config = {
        "from_attributes": True,
    }