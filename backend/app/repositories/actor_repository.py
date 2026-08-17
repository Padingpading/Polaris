"""Actor data access layer."""
from typing import Sequence

from sqlalchemy import func, select, update
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

    def delete_by_code(self, code: str) -> bool:
        """按 code 软删除：is_active = 0。"""
        stmt = update(Actor).where(Actor.code == code).values(is_active=False)
        result = self.db.execute(stmt)
        self.db.flush()
        return (result.rowcount or 0) > 0

    def page_list(self, *, offset: int, limit: int) -> tuple[Sequence[Actor], int]:
        count_stmt = select(func.count(Actor.id))
        list_stmt = (
            select(Actor).order_by(Actor.id.desc()).offset(offset).limit(limit)
        )
        total = self.db.scalar(count_stmt) or 0
        items = self.db.scalars(list_stmt).all()
        return items, total

    def page_list_query(self,name:str, offset:int, limit:int)->tuple[Sequence[Actor], int]:
        #数量
        filters = [Actor.status == 0]
        if name:
            filters.append(Actor.name.like("%{}%".format(name)))
        sum_count = select(func.count(Actor.id)).where(*filters);
        # 数据
        query = (
            select(Actor).where(*filters).order_by(Actor.id.desc())
            .offset(offset).limit(limit)
         )
        total  = self.db.scalar(sum_count)
        list  = self.db.scalars(query).all()
        return (list,total)
