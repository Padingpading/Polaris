"""Authentication endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_auth_service, get_current_user
from app.core.response import ApiResponse, success
from app.models.user import User
from app.schemas.auth import LoginOut, LoginRequest, UserBriefOut
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginOut], summary="User login")
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[LoginOut]:
    result = auth_service.login(payload)
    return success(result)


@router.post("/logout", response_model=ApiResponse[None], summary="User logout")
def logout(
    _: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[None]:
    """Stateless JWT logout: client discards the token."""
    return success(message="Logged out")


@router.get("/me", response_model=ApiResponse[UserBriefOut], summary="Current user profile")
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiResponse[UserBriefOut]:
    profile = auth_service.to_user_brief(current_user)
    return success(profile)
