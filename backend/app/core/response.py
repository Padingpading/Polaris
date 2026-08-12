"""Unified API response helpers."""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API envelope used by all endpoints."""

    code: int = Field(default=0, description="Business code, 0 means success")
    message: str = Field(default="ok")
    data: Optional[T] = None


def success(data: Any = None, message: str = "") -> ApiResponse[Any]:
    """Build a successful typed response."""
    return ApiResponse(code=0, message=message, data=data)


def fail(message: str, *, code: int = 1, data: Any = None) -> ApiResponse[Any]:
    """Build a failed typed response."""
    return ApiResponse(code=code, message=message, data=data)
