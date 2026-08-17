"""FastAPI dependency providers: auth, permissions, services."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.actor_repository import ActorRepository
from app.repositories.movie_repository import MovieRepository
from app.repositories.proxy_ip_pool_repository import ProxyIpPoolRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.actor_service import ActorService
from app.services.auth_service import AuthService
from app.services.movie_service import MovieService
from app.services.proxy_ip_pool_service import ProxyIpPoolService
from app.services.role_service import RoleService
from app.services.user_service import UserService

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Resolve the authenticated user from Bearer token."""
    if credentials is None or not credentials.credentials:
        raise UnauthorizedException("Missing authentication token")

    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise UnauthorizedException(str(exc)) from exc

    subject = payload.get("sub")
    if subject is None:
        raise UnauthorizedException("Invalid token payload")

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(subject))
    if user is None:
        raise UnauthorizedException("User not found")
    if not user.is_active:
        raise UnauthorizedException("User account is disabled")
    return user


def require_permissions(*permission_codes: str) -> Callable:
    """Dependency factory that enforces RBAC permission codes."""

    def checker(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if current_user.is_superuser:
            return current_user

        owned = AuthService.collect_permissions(current_user)
        missing = [code for code in permission_codes if code not in owned]
        if missing:
            raise ForbiddenException(f"Missing permissions: {', '.join(missing)}")
        return current_user

    return checker


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(UserRepository(db))


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(UserRepository(db))


def get_role_service(db: Annotated[Session, Depends(get_db)]) -> RoleService:
    return RoleService(RoleRepository(db))


def get_movie_service(db: Annotated[Session, Depends(get_db)]) -> MovieService:
    return MovieService(MovieRepository(db))

def get_actor_service(db: Annotated[Session, Depends(get_db)]) -> ActorService:
    return ActorService(ActorRepository(db))


def get_proxy_ip_pool_service(
    db: Annotated[Session, Depends(get_db)],
) -> ProxyIpPoolService:
    return ProxyIpPoolService(ProxyIpPoolRepository(db))
