"""Authentication related schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Username/password login payload."""

    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)


class TokenOut(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginOut(BaseModel):
    """Login response with token and user profile."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserBriefOut"


class UserBriefOut(BaseModel):
    """Lightweight user profile for auth responses."""

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_superuser: bool
    roles: list[str] = []
    permissions: list[str] = []

    model_config = {"from_attributes": True}


LoginOut.model_rebuild()
