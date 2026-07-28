"""Movie related schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    """Create movie request."""

    title: str = Field(..., min_length=1, max_length=128)
    director: Optional[str] = Field(default=None, max_length=64)
    genre: Optional[str] = Field(default=None, max_length=64)
    release_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    duration_minutes: Optional[int] = Field(default=None, ge=1, le=1000)
    rating: Optional[Decimal] = Field(default=None, ge=0, le=10)
    description: Optional[str] = None
    is_active: bool = True


class MovieUpdate(BaseModel):
    """Update movie request (partial)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=128)
    director: Optional[str] = Field(default=None, max_length=64)
    genre: Optional[str] = Field(default=None, max_length=64)
    release_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    duration_minutes: Optional[int] = Field(default=None, ge=1, le=1000)
    rating: Optional[Decimal] = Field(default=None, ge=0, le=10)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class MovieOut(BaseModel):
    """Movie detail response."""

    id: int
    title: str
    director: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    rating: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MovieQuery(BaseModel):
    """Movie list query filters."""

    keyword: Optional[str] = None
    genre: Optional[str] = None
    is_active: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
