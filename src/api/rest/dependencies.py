from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Header
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.core.exceptions import TokenException
from src.data.clients.postgres_client import get_db_session
from src.observability.logging.logger import get_logger, log_function
from src.schemas.auth_schema import TokenData


logger = get_logger(__name__)


async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    logger.info("Entering db_session_dependency")
    async for session in get_db_session():
        logger.info("db_session_dependency yielded session")
        yield session
    logger.info("Exiting db_session_dependency")


async def verify_token(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> TokenData:
    logger.info("Entering verify_token")
    if not authorization or not authorization.startswith("Bearer "):
        raise TokenException("Missing or invalid authorization header")

    access_token = authorization.removeprefix("Bearer ").strip()
    if not access_token:
        raise TokenException("Missing access token")

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

        token_data = TokenData(user_id=UUID(str(user_id_from_token)), role=token_role)
        logger.info("verify_token completed")
        return token_data
    except (JWTError, ValueError) as exc:
        raise TokenException(f"Invalid token: {exc}") from exc
    finally:
        logger.info("Exiting verify_token")
