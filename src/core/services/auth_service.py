from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.user_repository import UserRepository
from src.schemas.auth_schema import Token
from src.utils.jwt import create_access_token
from src.utils.security import verify_password


class AuthService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.repository = UserRepository(db_session)

    async def login(self, username: str, password: str) -> Token:
        user = await self.repository.get_by_name(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            )

        access_token = create_access_token(
            data={"user_id": str(user.id), "role": user.role}
        )
        return Token(access_token=access_token, token_type="bearer")