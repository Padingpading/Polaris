"""Actor management business logic."""

from app.models.actor import Actor
from app.repositories.actor_repository import ActorRepository
from app.schemas.actor import ActorCreate
from app.utls.random_utls import uuid, snowflake_id


class ActorService:
    """Actor CRUD operations."""

    def __init__(self, actor_repo: ActorRepository) -> None:
        self.actor_repo = actor_repo

    def create_actor(self, payload: ActorCreate) -> bool:
        actor = Actor(**payload.model_dump())
        actor.code = snowflake_id()
        self.actor_repo.save(actor)
        return True
