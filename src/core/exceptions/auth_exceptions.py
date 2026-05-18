from __future__ import annotations

from src.core.exceptions.base import BaseAppException


class InvalidCredentialsException(BaseAppException):
    """Raised when authentication credentials are invalid."""

    def __init__(self) -> None:
        super().__init__(
            message="Invalid username or password",
            status_code=401,
            error_code="INVALID_CREDENTIALS",
        )


class TokenException(BaseAppException):
    """Raised when token validation fails."""

    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(
            message=message,
            status_code=401,
            error_code="TOKEN_INVALID",
        )


class UnauthorizedException(BaseAppException):
    """Raised when user is not authorized to perform an action."""

    def __init__(self, message: str = "Not authorized") -> None:
        super().__init__(
            message=message,
            status_code=403,
            error_code="UNAUTHORIZED",
        )
