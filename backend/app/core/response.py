"""Unified API response helpers."""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API envelope used by all endpoints."""

    code: int = Field(default=0, description="Business code, 0 means success")
    message: str = Field(default="ok")
    data: Optional[T] = None


class PageResult(BaseModel, Generic[T]):
    """Paginated list payload."""

    items: list[T]
    total: int
    page: int
    page_size: int


def success(data: Any = None, message: str = "ok") -> dict[str, Any]:
    """Build a successful response dict."""
    return {"code": 0, "message": message, "data": data}


def fail(message: str, *, code: int = 1, data: Any = None) -> dict[str, Any]:
    """Build a failed response dict."""
    return {"code": code, "message": message, "data": data}
