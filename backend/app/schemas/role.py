"""Role and permission schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PermissionOut(BaseModel):
    """Permission response."""

    id: int
    code: str
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class RoleCreate(BaseModel):
    """Create role request."""

    code: str = Field(..., min_length=2, max_length=64)
    name: str = Field(..., min_length=2, max_length=64)
    description: Optional[str] = None
    permission_ids: list[int] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    """Update role request."""

    name: Optional[str] = Field(default=None, min_length=2, max_length=64)
    description: Optional[str] = None
    permission_ids: Optional[list[int]] = None


class RoleOut(BaseModel):
    """Role detail response."""

    id: int
    code: str
    name: str
    description: Optional[str] = None
    permissions: list[PermissionOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
