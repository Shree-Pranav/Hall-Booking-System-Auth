from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Cookie
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.core.exceptions import TokenException
from src.data.clients.postgres_client import get_db_session
from src.schemas.auth_schema import TokenData


async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session


async def verify_token(
    access_token: str | None = Cookie(default=None, alias="access_token"),
) -> TokenData:
    if not access_token:
        raise TokenException("Missing access token cookie")

    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id_from_token = payload.get("user_id")
        token_role = payload.get("role")

        if user_id_from_token is None or token_role is None:
            raise TokenException("Token payload is incomplete")

        return TokenData(user_id=UUID(str(user_id_from_token)), role=token_role)
    except (JWTError, ValueError) as exc:
        raise TokenException(f"Invalid token: {exc}") from exc
