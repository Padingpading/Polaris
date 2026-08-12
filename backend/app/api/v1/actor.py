"""Actor endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import get_actor_service
from app.core.response import ApiResponse, success
from app.schemas.actor import ActorCreate
from app.services.actor_service import ActorService

router = APIRouter()


@router.post("/create_actor", response_model=ApiResponse[bool], summary="Create actor")
def create_actor(
    req: ActorCreate,
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
) -> ApiResponse[bool]:
    data = actor_service.create_actor(req)
    return success(data)
