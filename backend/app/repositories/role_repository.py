"""Role and permission data access layer (sync Session)."""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.permission import Permission
from app.models.role import Role


class RoleRepository:
    """Persistence operations for roles and permissions."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_roles(self) -> Sequence[Role]:
        return self.db.scalars(
            select(Role).options(selectinload(Role.permissions)).order_by(Role.id.asc())
        ).all()

    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.scalar(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == role_id)
        )

    def get_by_code(self, code: str) -> Optional[Role]:
        return self.db.scalar(select(Role).where(Role.code == code))

    def create(self, role: Role) -> Role:
        self.db.add(role)
        self.db.flush()
        self.db.refresh(role, attribute_names=["permissions"])
        return role

    def delete(self, role: Role) -> None:
        self.db.delete(role)
        self.db.flush()

    def list_permissions(self) -> Sequence[Permission]:
        return self.db.scalars(select(Permission).order_by(Permission.id.asc())).all()

    def get_permissions_by_ids(self, permission_ids: list[int]) -> Sequence[Permission]:
        if not permission_ids:
            return []
        return self.db.scalars(
            select(Permission).where(Permission.id.in_(permission_ids))
        ).all()
