from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.user_repository import UserRepository
from src.utils.security import hash_password


logger = logging.getLogger(__name__)


async def seed_admin_user(db_session: AsyncSession) -> None:
    """Seed the database with a default admin user if it doesn't exist."""
    repository = UserRepository(db_session)

    admin_username = "admin"
    admin_password = "admin"

    # Check if admin user already exists
    existing_admin = await repository.get_by_name(admin_username)
    if existing_admin is not None:
        logger.info(f"Admin user '{admin_username}' already exists. Skipping seed.")
        return

    # Create admin user
    try:
        admin_user = await repository.create(
            name=admin_username,
            password_hash=hash_password(admin_password),
            role="admin",
        )
        logger.info(f"Admin user created successfully with username: {admin_username}")
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")
        raise
