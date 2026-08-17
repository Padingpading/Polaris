"""Aggregate v1 API routers."""

from fastapi import APIRouter

from app.api.v1 import actor, auth, movies, proxy_ip_pool, roles, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
api_router.include_router(actor.router, prefix="/actor", tags=["Actor"])
api_router.include_router(
    proxy_ip_pool.router, prefix="/proxy_ip_pool", tags=["ProxyIpPool"]
)
