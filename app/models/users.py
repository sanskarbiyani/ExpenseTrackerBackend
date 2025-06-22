from app.database.session import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Float

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    password = Column(String, nullable=False)
    credit = Column(Float, default=0, server_default="0")
    debit = Column(Float, default=0, server_default="0")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
