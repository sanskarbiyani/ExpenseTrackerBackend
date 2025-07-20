import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
ssl_context = ssl.create_default_context()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "ssl": ssl_context} if DATABASE_URL.startswith("sqlite") else {},
    echo=DEBUG,
)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

Base = declarative_base()
