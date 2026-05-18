from __future__ import annotations

import logging
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.core.exceptions import BaseAppException


logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> Response:
    """Global exception handler that converts all exceptions to JSON responses."""

    # Handle custom application exceptions
    if isinstance(exc, BaseAppException):
        logger.warning(
            f"Application exception: {exc.error_code} - {exc.message}",
            extra={"path": request.url.path, "status_code": exc.status_code},
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    # Handle validation errors from Pydantic
    if isinstance(exc, RequestValidationError):
        logger.warning(
            f"Validation error on {request.url.path}",
            extra={"errors": exc.errors()},
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {"validation_errors": exc.errors()},
            },
        )

    # Handle all other exceptions as 500 errors
    logger.error(
        f"Unhandled exception: {exc.__class__.__name__}",
        exc_info=exc,
        extra={"path": request.url.path},
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred",
            "details": {},
        },
    )
