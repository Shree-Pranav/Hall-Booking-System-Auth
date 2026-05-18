from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.postgres.user import User


class UserRepository:
	def __init__(self, db_session: AsyncSession) -> None:
		self.db_session = db_session

	async def get_by_id(self, user_id: UUID) -> User | None:
		result = await self.db_session.execute(select(User).where(User.id == user_id))
		return result.scalar_one_or_none()

	async def get_by_name(self, name: str) -> User | None:
		result = await self.db_session.execute(select(User).where(User.name == name))
		return result.scalar_one_or_none()

	async def list_all(self) -> list[User]:
		result = await self.db_session.execute(select(User).order_by(User.created_at.desc()))
		return list(result.scalars().all())

	async def create(
		self,
		*,
		name: str,
		password_hash: str,
		role: str,
	) -> User:
		user = User(
			name=name,
			password_hash=password_hash,
			role=role,
			is_active=True,
		)
		self.db_session.add(user)
		await self.db_session.flush()
		await self.db_session.refresh(user)
		return user

	async def update(
		self,
		user: User,
		*,
		name: str | None = None,
		password_hash: str | None = None,
		role: str | None = None,
		is_active: bool | None = None,
	) -> User:
		if name is not None:
			user.name = name
		if password_hash is not None:
			user.password_hash = password_hash
		if role is not None:
			user.role = role
		if is_active is not None:
			user.is_active = is_active

		await self.db_session.flush()
		await self.db_session.refresh(user)
		return user
