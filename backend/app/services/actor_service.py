"""Actor management business logic."""

from app.models.actor import Actor
from app.repositories.actor_repository import ActorRepository
from app.schemas.actor import ActorCreate, ActorOut


class ActorService:
    """Actor CRUD operations."""

    def __init__(self, actor_repo: ActorRepository) -> None:
        self.actor_repo = actor_repo

    def create_actor(self, payload: ActorCreate) -> ActorOut:
        actor = Actor(**payload.model_dump())
        created = self.actor_repo.save(actor)
        return True
