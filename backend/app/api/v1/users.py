"""User management endpoints (sync)."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_user_service, require_permissions
from app.core.response import ApiResponse, success
from app.models.user import User
from app.schemas.common import PageData
from app.schemas.user import UserCreate, UserOut, UserQuery, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=ApiResponse[PageData[UserOut]], summary="List users")
def list_users(
    _: Annotated[User, Depends(require_permissions("user:list"))],
    user_service: Annotated[UserService, Depends(get_user_service)],
    keyword: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ApiResponse[PageData[UserOut]]:
    query = UserQuery(keyword=keyword, is_active=is_active, page=page, page_size=page_size)
    data = user_service.list_users(query)
    return success(data)


@router.get("/{user_id}", response_model=ApiResponse[UserOut], summary="Get user detail")
def get_user(
    user_id: int,
    _: Annotated[User, Depends(require_permissions("user:read"))],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ApiResponse[UserOut]:
    data = user_service.get_user(user_id)
    return success(data)


@router.post("", response_model=ApiResponse[UserOut], summary="Create user")
def create_user(
    payload: UserCreate,
    _: Annotated[User, Depends(require_permissions("user:create"))],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ApiResponse[UserOut]:
    data = user_service.create_user(payload)
    return success(data, message="User created")


@router.put("/{user_id}", response_model=ApiResponse[UserOut], summary="Update user")
def update_user(
    user_id: int,
    payload: UserUpdate,
    _: Annotated[User, Depends(require_permissions("user:update"))],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ApiResponse[UserOut]:
    data = user_service.update_user(user_id, payload)
    return success(data, message="User updated")


@router.delete("/{user_id}", response_model=ApiResponse[None], summary="Delete user")
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(require_permissions("user:delete"))],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> ApiResponse[None]:
    user_service.delete_user(user_id, operator_id=current_user.id)
    return success(message="User deleted")
