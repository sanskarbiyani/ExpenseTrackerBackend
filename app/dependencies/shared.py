from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from app.database.session import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session