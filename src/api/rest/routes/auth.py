from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import verify_token
from src.config.settings import settings
from src.core.services.auth_service import AuthService
from src.core.services.user_service import UserService
from src.data.clients.postgres_client import get_db_session
from src.schemas.auth_schema import Token, TokenData
from src.schemas.user_schemas import UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Token:
    """Login endpoint that delegates authentication and token creation to service layer."""
    service = AuthService(session)
    login_result = await service.login(
        username=user_credentials.username,
        password=user_credentials.password,
    )

    response.set_cookie(
        key="access_token",
        value=login_result.access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return login_result


@router.get("/me", response_model=UserOut)
async def me(
    token_data: Annotated[TokenData, Depends(verify_token)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserOut:
    service = UserService(session)
    return await service.get_user(token_data.user_id)


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Logout endpoint that clears the access_token cookie."""
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="lax",
    )
    return {"message": "Logged out successfully"}
