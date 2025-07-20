import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.database.session import Base, engine
from app.routes import user, auth, transactions, accounts
from app.schemas.base_response import APIResponse
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "prod")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configure logging level
log_level = logging.DEBUG if DEBUG else logging.WARNING

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Suppress SQLAlchemy verbose logging unless in debug
if DEBUG:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
else:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

logging.getLogger("sqlalchemy.engine").propagate = False

app = FastAPI(debug=DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthCheck", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
    
@app.get("/db-connectivity", tags=["health"])
async def check_db_connectivity():
    """Health check endpoint."""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(success=False, error=exc.detail).model_dump(),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract errors from the exception
    error_messages = []
    for error in exc.errors():
        loc = " -> ".join(str(loc) for loc in error["loc"])
        msg = error["msg"]
        error_messages.append(f"{loc}: {msg}")

    return JSONResponse(
        status_code=422,
        content=APIResponse(success=False, error="; ".join(error_messages)).dict(),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content= APIResponse(success=False, error="Something went wrong").model_dump()
    )