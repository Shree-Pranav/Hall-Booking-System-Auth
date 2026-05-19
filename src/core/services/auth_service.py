from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import InvalidCredentialsException
from src.data.repositories.user_repository import UserRepository
from src.schemas.auth_schema import Token
from src.schemas.user_schemas import UserOut
from src.utils.jwt import create_access_token
from src.utils.security import verify_password


class AuthService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.repository = UserRepository(db_session)

    async def login(self, username: str, password: str) -> Token:
        """Authenticate user and return access token with user_id and role."""
        user = await self.repository.get_by_name(username)
        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            data={"user_id": str(user.id), "role": user.role}
        )
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserOut.model_validate(user),
        )