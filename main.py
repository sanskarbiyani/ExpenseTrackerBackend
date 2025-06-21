from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.session import Base, engine
from app.routes import user, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup code can be added here if needed

app = FastAPI(lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])