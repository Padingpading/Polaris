"""Application bootstrap: seed admin user, roles and permissions."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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
    ("movie:list", "List movies"),
    ("movie:read", "View movie"),
    ("movie:create", "Create movie"),
    ("movie:update", "Update movie"),
    ("movie:delete", "Delete movie"),
]


def _sync_permissions(session: Session) -> list[Permission]:
    """Ensure all default permissions exist and return full list."""
    existing = {
        item.code: item
        for item in session.scalars(select(Permission)).all()
    }
    created: list[Permission] = []
    for code, name in DEFAULT_PERMISSIONS:
        if code in existing:
            continue
        permission = Permission(code=code, name=name, description=name)
        session.add(permission)
        created.append(permission)
    if created:
        session.flush()
        for item in created:
            existing[item.code] = item
    return [existing[code] for code, _ in DEFAULT_PERMISSIONS if code in existing]


def _attach_role_permissions(session: Session, permissions: list[Permission]) -> None:
    """Attach missing permissions to built-in roles."""
    admin_role = session.scalar(
        select(Role).options(selectinload(Role.permissions)).where(Role.code == "admin")
    )
    viewer_role = session.scalar(
        select(Role).options(selectinload(Role.permissions)).where(Role.code == "viewer")
    )

    permission_map = {item.code: item for item in permissions}

    if admin_role is not None:
        owned = {item.code for item in admin_role.permissions}
        for permission in permissions:
            if permission.code not in owned:
                admin_role.permissions.append(permission)

    if viewer_role is not None:
        owned = {item.code for item in viewer_role.permissions}
        for code, permission in permission_map.items():
            if (code.endswith(":list") or code.endswith(":read")) and code not in owned:
                viewer_role.permissions.append(permission)

    session.flush()


def init_db(session: Session) -> None:
    """Create default RBAC data when empty, and sync permissions thereafter."""
    permissions = _sync_permissions(session)

    existing = session.scalar(select(User).limit(1))
    if existing is not None:
        _attach_role_permissions(session, permissions)
        session.commit()
        return

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
