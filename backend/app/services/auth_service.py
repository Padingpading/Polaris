"""Authentication business logic."""

from app.core.config import settings
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginOut, LoginRequest, UserBriefOut


class AuthService:
    """Handle login and current-user profile assembly."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    @staticmethod
    def collect_permissions(user: User) -> list[str]:
        """Flatten permission codes from user roles."""
        codes: set[str] = set()
        for role in user.roles:
            for permission in role.permissions:
                codes.add(permission.code)
        return sorted(codes)

    @staticmethod
    def collect_role_codes(user: User) -> list[str]:
        return sorted({role.code for role in user.roles})

    def to_user_brief(self, user: User) -> UserBriefOut:
        return UserBriefOut(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_superuser=user.is_superuser,
            roles=self.collect_role_codes(user),
            permissions=self.collect_permissions(user),
        )

    def login(self, payload: LoginRequest) -> LoginOut:
        user = self.user_repo.get_by_username(payload.username)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid username or password")
        if not user.is_active:
            raise BadRequestException("User account is disabled")

        token = create_access_token(
            subject=str(user.id),
            extra_claims={"username": user.username},
        )
        return LoginOut(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=self.to_user_brief(user),
        )
