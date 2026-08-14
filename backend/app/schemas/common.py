"""Common schema primitives."""

from typing import Annotated, Generic, TypeVar

from pydantic import AfterValidator, BaseModel, Field

T = TypeVar("T")


def int_range(ge: int, le: int, message: str) -> AfterValidator:
    """Integer range check with a concrete Chinese error message."""

    def _check(value: int) -> int:
        if value < ge or value > le:
            raise ValueError(message)
        return value

    return AfterValidator(_check)


def str_length(min_len: int, max_len: int, message: str) -> AfterValidator:
    """String length check with a concrete Chinese error message."""

    def _check(value: str) -> str:
        n = len(value)
        if n < min_len or n > max_len:
            raise ValueError(message)
        return value

    return AfterValidator(_check)


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
