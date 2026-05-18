from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.auth_service import AuthService
from src.data.clients.postgres_client import get_db_session
from src.schemas.auth_schema import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Token:
    """Login endpoint that delegates authentication and token creation to service layer."""
    service = AuthService(session)
    return await service.login(
        username=user_credentials.username,
        password=user_credentials.password,
    )
