"""User data access layer (sync Session)."""

from typing import Optional, Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.role import Role
from app.models.user import User


class UserRepository:
    """Persistence operations for users."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.scalar(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.id == user_id)
        )

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.scalar(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.username == username)
        )

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.scalar(select(User).where(User.email == email))

    def list_users(
        self,
        *,
        keyword: Optional[str] = None,
        is_active: Optional[bool] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[Sequence[User], int]:
        filters = []
        if keyword:
            like = f"%{keyword}%"
            filters.append(
                or_(
                    User.username.like(like),
                    User.email.like(like),
                    User.full_name.like(like),
                )
            )
        if is_active is not None:
            filters.append(User.is_active.is_(is_active))

        count_stmt = select(func.count(User.id))
        list_stmt = (
            select(User)
            .options(selectinload(User.roles))
            .order_by(User.id.desc())
            .offset(offset)
            .limit(limit)
        )
        if filters:
            count_stmt = count_stmt.where(*filters)
            list_stmt = list_stmt.where(*filters)

        total = self.db.scalar(count_stmt) or 0
        items = self.db.scalars(list_stmt).all()
        return items, total

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user, attribute_names=["roles"])
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.flush()

    def get_roles_by_ids(self, role_ids: list[int]) -> Sequence[Role]:
        if not role_ids:
            return []
        return self.db.scalars(select(Role).where(Role.id.in_(role_ids))).all()
