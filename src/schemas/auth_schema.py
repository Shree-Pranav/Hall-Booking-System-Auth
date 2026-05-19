from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from src.schemas.user_schemas import UserOut


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class TokenData(BaseModel):
    user_id: UUID
    role: Literal["admin", "user"]


class TokenPayload(TokenData):
    exp: int