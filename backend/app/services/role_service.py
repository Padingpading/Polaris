"""Role management business logic."""

from app.core.exceptions import ConflictException, NotFoundException
from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import PermissionOut, RoleCreate, RoleOut, RoleUpdate


class RoleService:
    """Role and permission operations."""

    def __init__(self, role_repo: RoleRepository) -> None:
        self.role_repo = role_repo

    def list_roles(self) -> list[RoleOut]:
        roles = self.role_repo.list_roles()
        return [RoleOut.model_validate(role) for role in roles]

    def list_permissions(self) -> list[PermissionOut]:
        permissions = self.role_repo.list_permissions()
        return [PermissionOut.model_validate(item) for item in permissions]

    def create_role(self, payload: RoleCreate) -> RoleOut:
        if self.role_repo.get_by_code(payload.code):
            raise ConflictException("Role code already exists")

        permissions = self.role_repo.get_permissions_by_ids(payload.permission_ids)
        if len(permissions) != len(set(payload.permission_ids)):
            raise NotFoundException("One or more permissions not found")

        role = Role(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            permissions=list(permissions),
        )
        created = self.role_repo.create(role)
        created = self.role_repo.get_by_id(created.id)
        return RoleOut.model_validate(created)

    def update_role(self, role_id: int, payload: RoleUpdate) -> RoleOut:
        role = self.role_repo.get_by_id(role_id)
        if role is None:
            raise NotFoundException("Role not found")

        data = payload.model_dump(exclude_unset=True)
        permission_ids = data.pop("permission_ids", None)

        for field, value in data.items():
            setattr(role, field, value)

        if permission_ids is not None:
            permissions = self.role_repo.get_permissions_by_ids(permission_ids)
            if len(permissions) != len(set(permission_ids)):
                raise NotFoundException("One or more permissions not found")
            role.permissions = list(permissions)

        self.role_repo.db.flush()
        role = self.role_repo.get_by_id(role_id)
        return RoleOut.model_validate(role)

    def delete_role(self, role_id: int) -> None:
        role = self.role_repo.get_by_id(role_id)
        if role is None:
            raise NotFoundException("Role not found")
        if role.code == "admin":
            raise ConflictException("Cannot delete built-in admin role")
        self.role_repo.delete(role)
