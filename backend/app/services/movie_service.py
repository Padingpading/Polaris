"""Movie management business logic."""

from app.core.exceptions import NotFoundException
from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository
from app.schemas.common import PageData
from app.schemas.movie import MovieCreate, MovieOut, MovieQuery, MovieUpdate


class MovieService:
    """Movie CRUD operations."""

    def __init__(self, movie_repo: MovieRepository) -> None:
        self.movie_repo = movie_repo

    def get_movie(self, movie_id: int) -> MovieOut:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise NotFoundException("Movie not found")
        return MovieOut.model_validate(movie)

    def list_movies(self, query: MovieQuery) -> PageData[MovieOut]:
        offset = (query.page - 1) * query.page_size
        items, total = self.movie_repo.list_movies(
            keyword=query.keyword,
            genre=query.genre,
            is_active=query.is_active,
            offset=offset,
            limit=query.page_size,
        )
        return PageData(
            items=[MovieOut.model_validate(item) for item in items],
            total=total,
            page=query.page,
            page_size=query.page_size,
        )

    def create_movie(self, payload: MovieCreate) -> MovieOut:
        movie = Movie(**payload.model_dump())
        created = self.movie_repo.create(movie)
        return MovieOut.model_validate(created)

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> MovieOut:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise NotFoundException("Movie not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.movie_repo.db.flush()
        self.movie_repo.db.refresh(movie)
        return MovieOut.model_validate(movie)

    def delete_movie(self, movie_id: int) -> None:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise NotFoundException("Movie not found")
        self.movie_repo.delete(movie)
