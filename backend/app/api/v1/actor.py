"""Actor endpoints (sync)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_actor_service
from app.core.response import ApiResponse, success
from app.schemas.actor import ActorCreate, ActorOut, ActorUpdate
from app.schemas.common import PageData
from app.services.actor_service import ActorService

router = APIRouter()


@router.post("/create_actor", response_model=ApiResponse[bool], summary="Create actor")
def create_actor(
    req: ActorCreate,
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
) -> ApiResponse[bool]:
    data = actor_service.create_actor(req)
    return success(data)


@router.post("/update_actor", response_model=ApiResponse[bool], summary="Update actor")
def update_actor(
    req: ActorUpdate,
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
) -> ApiResponse[bool]:
    data = actor_service.update_actor(req)
    return success(data)


@router.get("/find_by_code", response_model=ApiResponse[ActorOut], summary="Find actor by code")
def find_by_code(
    code: str,
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
) -> ApiResponse[ActorOut]:
    data = actor_service.find_by_code(code)
    return success(data)


@router.get("/delete_by_code", response_model=ApiResponse[bool], summary="Delete actor by code")
def delete_by_code(
    code: str,
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
) -> ApiResponse[bool]:
    data = actor_service.delete_by_code(code)
    return success(data)


@router.get("/page_list", response_model=ApiResponse[PageData[ActorOut]], summary="Page actor")
def page_list(
    actor_service: Annotated[ActorService, Depends(get_actor_service)],
    name:str,
    page_no: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ApiResponse[PageData[ActorOut]]:
    data = actor_service.page_list(name,page_no, page_size)
    return success(data)
