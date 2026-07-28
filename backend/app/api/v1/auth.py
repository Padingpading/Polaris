"""Authentication endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_auth_service, get_current_user
from app.core.response import success
from app.models.user import User
from app.schemas.auth import LoginOut, LoginRequest, UserBriefOut
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=None, summary="User login")
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    result: LoginOut = auth_service.login(payload)
    return success(result.model_dump())


@router.post("/logout", response_model=None, summary="User logout")
def logout(
    _: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Stateless JWT logout: client discards the token."""
    return success(message="Logged out")


@router.get("/me", response_model=None, summary="Current user profile")
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    profile: UserBriefOut = auth_service.to_user_brief(current_user)
    return success(profile.model_dump())
