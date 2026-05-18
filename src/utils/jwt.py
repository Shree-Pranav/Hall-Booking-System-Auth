from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from jose import JWTError, jwt

from src.config.settings import settings
from src.schemas.auth_schema import TokenData


def create_access_token(data: dict) -> str:
    """Create a JWT access token with expiry."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """Verify and decode a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_raw = payload.get("user_id")
        role_raw = payload.get("role")
        if user_id_raw is None or role_raw is None:
            raise credentials_exception

        token_data = TokenData(
            user_id=UUID(str(user_id_raw)),
            role=role_raw,
        )
    except (JWTError, ValueError):
        raise credentials_exception

    return token_data