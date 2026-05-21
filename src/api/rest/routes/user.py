from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.user_service import UserService
from src.data.clients.postgres_client import get_db_session
from src.observability.logging.logger import get_logger, log_function
from src.schemas.user_schemas import UserCreate, UserOut, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger(__name__)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@log_function(logger)
async def create_user(
    user_in: UserCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> UserOut:
    service = UserService(db_session)
    return await service.create_user(user_in)


@router.get("/{user_id}", response_model=UserOut)
@log_function(logger)
async def get_user(
    user_id: UUID,
    db_session: AsyncSession = Depends(get_db_session),
) -> UserOut:
    service = UserService(db_session)
    return await service.get_user(user_id)


@router.get("", response_model=list[UserOut])
@log_function(logger)
async def list_users(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[UserOut]:
    service = UserService(db_session)
    return await service.list_users()


@router.patch("/{user_id}", response_model=UserOut)
@log_function(logger)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db_session: AsyncSession = Depends(get_db_session),
) -> UserOut:
    service = UserService(db_session)
    return await service.update_user(user_id, user_update)
