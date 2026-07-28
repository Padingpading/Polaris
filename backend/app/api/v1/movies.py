"""Movie management endpoints (sync)."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_movie_service, require_permissions
from app.core.response import ApiResponse, success
from app.models.user import User
from app.schemas.common import PageData
from app.schemas.movie import MovieCreate, MovieOut, MovieQuery, MovieUpdate
from app.services.movie_service import MovieService

router = APIRouter()


@router.get("", response_model=ApiResponse[PageData[MovieOut]], summary="List movies")
def list_movies(
    _: Annotated[User, Depends(require_permissions("movie:list"))],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
    keyword: Optional[str] = Query(default=None),
    genre: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ApiResponse[PageData[MovieOut]]:
    query = MovieQuery(
        keyword=keyword,
        genre=genre,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )
    data = movie_service.list_movies(query)
    return success(data)


@router.get("/{movie_id}", response_model=ApiResponse[MovieOut], summary="Get movie detail")
def get_movie(
    movie_id: int,
    _: Annotated[User, Depends(require_permissions("movie:read"))],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> ApiResponse[MovieOut]:
    data = movie_service.get_movie(movie_id)
    return success(data)


@router.post("", response_model=ApiResponse[MovieOut], summary="Create movie")
def create_movie(
    payload: MovieCreate,
    _: Annotated[User, Depends(require_permissions("movie:create"))],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> ApiResponse[MovieOut]:
    data = movie_service.create_movie(payload)
    return success(data, message="Movie created")


@router.put("/{movie_id}", response_model=ApiResponse[MovieOut], summary="Update movie")
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    _: Annotated[User, Depends(require_permissions("movie:update"))],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> ApiResponse[MovieOut]:
    data = movie_service.update_movie(movie_id, payload)
    return success(data, message="Movie updated")


@router.delete("/{movie_id}", response_model=ApiResponse[None], summary="Delete movie")
def delete_movie(
    movie_id: int,
    _: Annotated[User, Depends(require_permissions("movie:delete"))],
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> ApiResponse[None]:
    movie_service.delete_movie(movie_id)
    return success(message="Movie deleted")
