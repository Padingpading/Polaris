"""Actor management business logic."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal

from app.core.exceptions import AppException
from app.models.actor import Actor
from app.repositories.actor_repository import ActorRepository
from app.schemas.actor import ActorCreate, ActorUpdate, ActorOut
from app.utls.random_utls import snowflake_id


def _parse_gender(gender_desc: str) -> int:
    if gender_desc == "男":
        return 1
    if gender_desc == "女":
        return 2
    return 0


def _parse_tags(tags: str) -> str:
    if not tags:
        return ""
    tag_list = []
    # for tag in tags.split(","):
    #     strip = tag.strip()
    #     if strip:
    #         tag_list.append(strip)
    # tag_list = [item.strip() for item in tags.split(",") if item.strip()]
    tag_list = [ tag  for tag in tags.split(",") if tag ]
    return json.dumps(tag_list, ensure_ascii=False) if tag_list else ""


def _parse_birth_date(birth_date: str):
    if not birth_date:
        return None
    return datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S").date()


def _parse_debut_time(debut_time: str):
    if not debut_time:
        return None
    # 支持 "15:30:00" 或 "2026-08-12 15:30:00"
    if " " in debut_time:
        return datetime.strptime(debut_time, "%Y-%m-%d %H:%M:%S").time()
    return datetime.strptime(debut_time, "%H:%M:%S").time()


class ActorService:
    """Actor CRUD operations."""

    def __init__(self, actor_repo: ActorRepository) -> None:
        self.actor_repo = actor_repo

    def create_actor(self, payload: ActorCreate) -> bool:
        actor = Actor()
        actor.code = snowflake_id()
        actor.name = payload.name
        actor.stage_name = payload.stage_name
        actor.age = payload.age
        actor.fan_count = payload.fan_count
        actor.view_count = payload.view_count
        actor.tags = _parse_tags(payload.tags)
        actor.bio = payload.bio
        actor.gender = _parse_gender(payload.gender_desc)
        actor.height_cm = Decimal(str(payload.height_cm))
        actor.rating = Decimal(str(payload.rating))
        actor.debut_time = _parse_debut_time(payload.debut_time)
        actor.birth_date = _parse_birth_date(payload.birth_date)
        actor.last_login_at = datetime.now()
        self.actor_repo.save(actor)
        return True

    def update_actor(self, req: ActorUpdate) -> bool:
        if not req.code:
            raise AppException("code 不能为空")

        actor = self.actor_repo.find_by_code(req.code)
        if actor is None:
            raise AppException("未查询到演员信息")

        ok = self.actor_repo.update_by_code(
            req.code,
            name=req.name,
            stage_name=req.stage_name,
            age=req.age,
            fan_count=req.fan_count,
            view_count=req.view_count,
            tags=_parse_tags(req.tags),
            bio=req.bio,
            gender=_parse_gender(req.gender_desc),
            height_cm=Decimal(str(req.height_cm)),
            rating=Decimal(str(req.rating)),
            debut_time=_parse_debut_time(req.debut_time),
            birth_date=_parse_birth_date(req.birth_date),
            last_login_at=datetime.now(),
        )
        if not ok:
            raise AppException("更新失败")
        return True

    def find_by_code(self, code):
        # 根据code查询
        if not code:
            raise AppException("code 不能为空")
        actor = self.actor_repo.find_by_code(code)
        resp = ActorOut()

        pass
