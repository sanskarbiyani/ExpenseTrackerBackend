from datetime import datetime
from app.database.session import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.accounts import Account

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    credit: Mapped[float] = mapped_column(Float, default=0, server_default="0")
    debit: Mapped[float] = mapped_column(Float, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user", cascade="all, delete-orphan")
