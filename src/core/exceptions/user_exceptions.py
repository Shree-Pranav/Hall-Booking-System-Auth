from __future__ import annotations

from src.core.exceptions.base import BaseAppException


class UserAlreadyExistsException(BaseAppException):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, username: str) -> None:
        super().__init__(
            message=f"User '{username}' already exists",
            status_code=409,
            error_code="USER_ALREADY_EXISTS",
            details={"username": username},
        )


class UserNotFoundException(BaseAppException):
    """Raised when a user is not found."""

    def __init__(self, user_id: str | None = None, username: str | None = None) -> None:
        details = {}
        if user_id:
            details["user_id"] = user_id
        if username:
            details["username"] = username

        super().__init__(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND",
            details=details,
        )


class InvalidUserDataException(BaseAppException):
    """Raised when user data is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=400,
            error_code="INVALID_USER_DATA",
        )
