"""Role and permission endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_role_service, require_permissions
from app.core.response import ApiResponse, success
from app.models.user import User
from app.schemas.role import PermissionOut, RoleCreate, RoleOut, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()


@router.get("", response_model=ApiResponse[list[RoleOut]], summary="List roles")
def list_roles(
    _: Annotated[User, Depends(require_permissions("role:list"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> ApiResponse[list[RoleOut]]:
    data = role_service.list_roles()
    return success(data)


@router.get(
    "/permissions",
    response_model=ApiResponse[list[PermissionOut]],
    summary="List permissions",
)
def list_permissions(
    _: Annotated[User, Depends(require_permissions("role:list"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> ApiResponse[list[PermissionOut]]:
    data = role_service.list_permissions()
    return success(data)


@router.post("", response_model=ApiResponse[RoleOut], summary="Create role")
def create_role(
    payload: RoleCreate,
    _: Annotated[User, Depends(require_permissions("role:create"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> ApiResponse[RoleOut]:
    data = role_service.create_role(payload)
    return success(data, message="Role created")


@router.put("/{role_id}", response_model=ApiResponse[RoleOut], summary="Update role")
def update_role(
    role_id: int,
    payload: RoleUpdate,
    _: Annotated[User, Depends(require_permissions("role:update"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> ApiResponse[RoleOut]:
    data = role_service.update_role(role_id, payload)
    return success(data, message="Role updated")


@router.delete("/{role_id}", response_model=ApiResponse[None], summary="Delete role")
def delete_role(
    role_id: int,
    _: Annotated[User, Depends(require_permissions("role:delete"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> ApiResponse[None]:
    role_service.delete_role(role_id)
    return success(message="Role deleted")
