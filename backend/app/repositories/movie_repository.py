"""Movie data access layer."""

from typing import Optional, Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.movie import Movie


class MovieRepository:
    """Persistence operations for movies."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return self.db.scalar(select(Movie).where(Movie.id == movie_id))

    def list_movies(
            self,
            *,
            keyword: Optional[str] = None,
            genre: Optional[str] = None,
            is_active: Optional[bool] = None,
            offset: int = 0,
            limit: int = 10,
    ) -> tuple[Sequence[Movie], int]:
        filters = []
        if keyword:
            like = f"%{keyword}%"
            filters.append(
                or_(
                    Movie.title.like(like),
                    Movie.director.like(like),
                    Movie.description.like(like),
                )
            )
        if genre:
            filters.append(Movie.genre == genre)
        if is_active is not None:
            filters.append(Movie.is_active.is_(is_active))

        count_stmt = select(func.count(Movie.id))
        list_stmt = (
            select(Movie).order_by(Movie.id.desc()).offset(offset).limit(limit)
        )
        if filters:
            count_stmt = count_stmt.where(*filters)
            list_stmt = list_stmt.where(*filters)

        total = self.db.scalar(count_stmt) or 0
        items = self.db.scalars(list_stmt).all()
        return items, total

    def create(self, movie: Movie) -> Movie:
        self.db.add(movie)
        self.db.flush()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.flush()
