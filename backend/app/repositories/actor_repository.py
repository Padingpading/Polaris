"""Actor data access layer."""

from sqlalchemy.orm import Session

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
