"""Common schema primitives."""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageQuery(BaseModel):
    """Pagination query parameters."""

    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")


class PageData(BaseModel, Generic[T]):
    """Paginated response data."""

    items: list[T]
    total: int
    page: int
    page_size: int


class MessageOut(BaseModel):
    """Simple message payload."""

    message: str
