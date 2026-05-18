from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.data.clients.postgres_client import get_or_create_engine
from src.api.rest.routes.health import router as health_router 
from src.api.rest.routes.user import router as user_router
from src.api.rest.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    engine = await get_or_create_engine()
    yield
    await engine.dispose()
    print("Shutting down the application...")


app = FastAPI(title="Hall Booking System Auth API", lifespan=lifespan)

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