from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Float, Enum as SQLEnum
from enum import IntEnum

from app.database.session import Base

class TransactionType(IntEnum):
    INCOME = 1
    EXPENSE = 2
    TRANSFER = 3

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    title = Column(String, nullable=False, default="Not added.", server_default="Not added.")
    description = Column(String, nullable=True)
    transaction_type = Column(Integer, nullable=False, default=TransactionType.EXPENSE, server_default="2")  # 1 for income, 2 for expense
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Transaction (id={self.id}, user_id={self.user_id}, amount={self.amount}, description={self.description})>"