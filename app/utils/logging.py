from sqlalchemy.ext.asyncio import AsyncSession
from app.models.logs import Log
from app.database.session import SessionLocal

async def log_to_db(error_message: str, level: str, method: str, user_id: int, action: str):
    """Log an error message to the database."""
    log_entry = Log(user_id=user_id, level=level, method_name=method, action=action, log=error_message)
    async with SessionLocal() as db:
        try:
            db.add(log_entry)
            await db.commit()
        except Exception as e:
            # If commit fails, we can log the error to console or handle it accordingly
            print(f"Failed to log error to database: {e}")