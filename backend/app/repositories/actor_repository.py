"""Actor data access layer."""
from sqlalchemy import select, update
from sqlalchemy.orm import Session, DeclarativeBase

from app.models.actor import Actor


class ActorRepository:
    """Persistence operations for actors."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, actor: Actor) -> Actor:
        self.db.add(actor)
        self.db.flush()
        self.db.refresh(actor)
        return actor

    def find_by_code(self, code: str) -> Actor | None:
        stmt = select(Actor).where(Actor.code == code)
        return self.db.scalars(stmt).first()

    def update_by_code(self, code: str, **values) -> bool:
        """根据 code 直接更新字段。例: update_by_code(code, name='张三', age=30)"""
        if not values:
            return False
        stmt = update(Actor).where(Actor.code == code).values(**values)
        result = self.db.execute(stmt)
        self.db.flush()
        return (result.rowcount or 0) > 0