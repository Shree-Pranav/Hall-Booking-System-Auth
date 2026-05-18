from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# =========================
# Base Schemas
# =========================

class UserBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="User full name"
    )

    role: Literal["admin", "user"]


# =========================
# Create User
# =========================

class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Password must be between 8 and 72 characters"
    )





# =========================
# User Response
# =========================

class UserOut(UserBase):
    id: UUID
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )




# =========================
# Optional User Update
# =========================

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=72
    )

    role: Literal["admin", "user"] | None = None

    is_active: bool | None = None