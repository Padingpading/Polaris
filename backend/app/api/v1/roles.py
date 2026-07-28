"""Role and permission endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_role_service, require_permissions
from app.core.response import success
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()


@router.get("", response_model=None, summary="List roles")
def list_roles(
    _: Annotated[User, Depends(require_permissions("role:list"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> dict:
    data = role_service.list_roles()
    return success([item.model_dump() for item in data])


@router.get("/permissions", response_model=None, summary="List permissions")
def list_permissions(
    _: Annotated[User, Depends(require_permissions("role:list"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> dict:
    data = role_service.list_permissions()
    return success([item.model_dump() for item in data])


@router.post("", response_model=None, summary="Create role")
def create_role(
    payload: RoleCreate,
    _: Annotated[User, Depends(require_permissions("role:create"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> dict:
    data = role_service.create_role(payload)
    return success(data.model_dump(), message="Role created")


@router.put("/{role_id}", response_model=None, summary="Update role")
def update_role(
    role_id: int,
    payload: RoleUpdate,
    _: Annotated[User, Depends(require_permissions("role:update"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> dict:
    data = role_service.update_role(role_id, payload)
    return success(data.model_dump(), message="Role updated")


@router.delete("/{role_id}", response_model=None, summary="Delete role")
def delete_role(
    role_id: int,
    _: Annotated[User, Depends(require_permissions("role:delete"))],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> dict:
    role_service.delete_role(role_id)
    return success(message="Role deleted")
