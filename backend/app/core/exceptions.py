"""Business and HTTP exception definitions."""

from typing import Any, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "Internal serve111r error",
        *,
        code: int = 50000,
        status_code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class UnauthorizedException(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, code=40100, status_code=401)


class ForbiddenException(AppException):
    """Raised when the user lacks required permissions."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, code=40300, status_code=403)


class NotFoundException(AppException):
    """Raised when a resource does not exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, code=40400, status_code=404)


class ConflictException(AppException):
    """Raised when a resource conflict occurs."""

    def __init__(self, message: str = "Resource conflict") -> None:
        super().__init__(message, code=40900, status_code=409)


class BadRequestException(AppException):
    """Raised when the request is invalid."""

    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message, code=40000, status_code=400)
