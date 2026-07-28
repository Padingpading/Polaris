"""User related schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Create user request body."""

    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=128)
    is_active: bool = True
    role_ids: list[int] = Field(default_factory=list)


class UserUpdate(BaseModel):
    """Update user request body (partial)."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(default=None, max_length=128)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)
    role_ids: Optional[list[int]] = None


class RoleBriefOut(BaseModel):
    """Role brief embedded in user responses."""

    id: int
    code: str
    name: str

    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    """User detail response."""

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    roles: list[RoleBriefOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserQuery(BaseModel):
    """User list query filters."""

    keyword: Optional[str] = Field(default=None, description="Search username/email/full_name")
    is_active: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
