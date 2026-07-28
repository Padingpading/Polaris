"""Application bootstrap: seed admin user, roles and permissions."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User

DEFAULT_PERMISSIONS = [
    ("user:list", "List users"),
    ("user:read", "View user"),
    ("user:create", "Create user"),
    ("user:update", "Update user"),
    ("user:delete", "Delete user"),
    ("role:list", "List roles"),
    ("role:create", "Create role"),
    ("role:update", "Update role"),
    ("role:delete", "Delete role"),
]


def init_db(session: Session) -> None:
    """Create default RBAC data when database is empty."""
    existing = session.scalar(select(User).limit(1))
    if existing is not None:
        return

    permissions: list[Permission] = []
    for code, name in DEFAULT_PERMISSIONS:
        permissions.append(Permission(code=code, name=name, description=name))
    session.add_all(permissions)
    session.flush()

    admin_role = Role(
        code="admin",
        name="Administrator",
        description="Full system access",
        permissions=permissions,
    )
    viewer_role = Role(
        code="viewer",
        name="Viewer",
        description="Read-only access",
        permissions=[
            p for p in permissions if p.code.endswith(":list") or p.code.endswith(":read")
        ],
    )
    session.add_all([admin_role, viewer_role])
    session.flush()

    admin_user = User(
        username="admin",
        email="admin@polaris.local",
        hashed_password=hash_password("Admin@123"),
        full_name="System Admin",
        is_active=True,
        is_superuser=True,
        roles=[admin_role],
    )
    demo_user = User(
        username="viewer",
        email="viewer@polaris.local",
        hashed_password=hash_password("Viewer@123"),
        full_name="Demo Viewer",
        is_active=True,
        is_superuser=False,
        roles=[viewer_role],
    )
    session.add_all([admin_user, demo_user])
    session.commit()
