from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship

from app.database.session import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, default="Not added.", server_default="Not added.")
    description = Column(String, nullable=True)
    balance = Column(Float, nullable=False, default=0.0, server_default="0.0")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    user = relationship("User", back_populates="accounts")

    def __repr__(self):
        return f"<Account (id={self.id}, user_id={self.user_id}, name={self.name}, balance={self.balance})>"