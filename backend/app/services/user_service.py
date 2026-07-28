"""User management business logic."""

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.common import PageData
from app.schemas.user import UserCreate, UserOut, UserQuery, UserUpdate


class UserService:
    """User CRUD operations."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> UserOut:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundException("User not found")
        return UserOut.model_validate(user)

    def list_users(self, query: UserQuery) -> PageData[UserOut]:
        offset = (query.page - 1) * query.page_size
        items, total = self.user_repo.list_users(
            keyword=query.keyword,
            is_active=query.is_active,
            offset=offset,
            limit=query.page_size,
        )
        return PageData(
            items=[UserOut.model_validate(item) for item in items],
            total=total,
            page=query.page,
            page_size=query.page_size,
        )

    def create_user(self, payload: UserCreate) -> UserOut:
        if self.user_repo.get_by_username(payload.username):
            raise ConflictException("Username already exists")
        if self.user_repo.get_by_email(payload.email):
            raise ConflictException("Email already exists")

        roles = self.user_repo.get_roles_by_ids(payload.role_ids)
        if len(roles) != len(set(payload.role_ids)):
            raise NotFoundException("One or more roles not found")

        user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            is_active=payload.is_active,
            roles=list(roles),
        )
        created = self.user_repo.create(user)
        created = self.user_repo.get_by_id(created.id)
        return UserOut.model_validate(created)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserOut:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundException("User not found")

        data = payload.model_dump(exclude_unset=True)
        role_ids = data.pop("role_ids", None)
        password = data.pop("password", None)

        if "email" in data and data["email"] != user.email:
            existing = self.user_repo.get_by_email(data["email"])
            if existing and existing.id != user.id:
                raise ConflictException("Email already exists")

        for field, value in data.items():
            setattr(user, field, value)

        if password:
            user.hashed_password = hash_password(password)

        if role_ids is not None:
            roles = self.user_repo.get_roles_by_ids(role_ids)
            if len(roles) != len(set(role_ids)):
                raise NotFoundException("One or more roles not found")
            user.roles = list(roles)

        self.user_repo.db.flush()
        user = self.user_repo.get_by_id(user_id)
        return UserOut.model_validate(user)

    def delete_user(self, user_id: int, *, operator_id: int) -> None:
        if user_id == operator_id:
            raise ConflictException("Cannot delete your own account")
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundException("User not found")
        if user.is_superuser:
            raise ConflictException("Cannot delete superuser account")
        self.user_repo.delete(user)
