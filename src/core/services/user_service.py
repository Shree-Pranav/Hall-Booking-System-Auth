from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.user_repository import UserRepository
from src.schemas.user_schemas import UserCreate, UserOut, UserUpdate
from src.utils.security import hash_password


class UserService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.repository = UserRepository(db_session)

    async def create_user(self, user_in: UserCreate) -> UserOut:
        existing_user = await self.repository.get_by_name(user_in.name)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        created_user = await self.repository.create(
            name=user_in.name,
            password_hash=hash_password(user_in.password),
            role=user_in.role,
        )
        return UserOut.model_validate(created_user)

    async def get_user(self, user_id: UUID) -> UserOut:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut.model_validate(user)

    async def list_users(self) -> list[UserOut]:
        users = await self.repository.list_all()
        return [UserOut.model_validate(user) for user in users]

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserOut:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_update.name is not None:
            existing_user = await self.repository.get_by_name(user_update.name)
            if existing_user is not None and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User already exists",
                )

        updated_user = await self.repository.update(
            user,
            name=user_update.name,
            password_hash=hash_password(user_update.password) if user_update.password else None,
            role=user_update.role,
            is_active=user_update.is_active,
        )
        return UserOut.model_validate(updated_user)
