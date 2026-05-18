from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.clients.postgres_client import get_or_create_engine
from src.api.rest.routes.health import router as health_router 
from src.api.rest.routes.user import router as user_router
from src.api.rest.routes.auth import router as auth_router
from src.api.middleware.error_handler import global_exception_handler
from src.core.exceptions import BaseAppException
from src.data.seed import seed_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    engine = await get_or_create_engine()
    
    # Seed admin user on startup
    async with AsyncSession(engine) as session:
        await seed_admin_user(session)
    
    yield
    await engine.dispose()
    print("Shutting down the application...")


app = FastAPI(title="Hall Booking System Auth API", lifespan=lifespan)

# Register global exception handlers
app.add_exception_handler(BaseAppException, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hall Booking System API!"}

app.include_router(health_router)
app.include_router(user_router)
app.include_router(auth_router)