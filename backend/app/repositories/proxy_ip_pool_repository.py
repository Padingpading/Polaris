"""Proxy IP pool data access layer."""

from typing import Optional, Sequence

from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import Session

from app.models.proxy_ip_pool import ProxyIpPool


class ProxyIpPoolRepository:
    """Persistence operations for proxy_ip_pool."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, row: ProxyIpPool) -> ProxyIpPool:
        self.db.add(row)
        self.db.flush()
        self.db.refresh(row)
        return row

    def find_by_id(self, row_id: int) -> ProxyIpPool | None:
        stmt = select(ProxyIpPool).where(
            ProxyIpPool.id == row_id,
            ProxyIpPool.status == 0,
        )
        return self.db.scalar(stmt)

    def update_by_id(self, row_id: int, **values) -> bool:
        if not values:
            return False
        stmt = (
            update(ProxyIpPool)
            .where(ProxyIpPool.id == row_id, ProxyIpPool.status == 0)
            .values(**values)
        )
        result = self.db.execute(stmt)
        self.db.flush()
        return (result.rowcount or 0) > 0

    def delete_by_id(self, row_id: int) -> bool:
        """软删除：status = 1。"""
        stmt = (
            update(ProxyIpPool)
            .where(ProxyIpPool.id == row_id, ProxyIpPool.status == 0)
            .values(status=1)
        )
        result = self.db.execute(stmt)
        self.db.flush()
        return (result.rowcount or 0) > 0

    def page_list(
        self,
        *,
        keyword: Optional[str] = None,
        usage_status: Optional[bool] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[Sequence[ProxyIpPool], int]:
        filters = [ProxyIpPool.status == 0]
        if keyword:
            like = f"%{keyword}%"
            filters.append(
                or_(
                    ProxyIpPool.ip.like(like),
                    ProxyIpPool.city.like(like),
                    ProxyIpPool.remark.like(like),
                )
            )
        if usage_status is not None:
            filters.append(ProxyIpPool.usage_status.is_(usage_status))

        count_stmt = select(func.count(ProxyIpPool.id)).where(*filters)
        list_stmt = (
            select(ProxyIpPool)
            .where(*filters)
            .order_by(ProxyIpPool.id.desc())
            .offset(offset)
            .limit(limit)
        )
        total = self.db.scalar(count_stmt) or 0
        items = self.db.scalars(list_stmt).all()
        return items, total

    def query_by_ids(self, row_ids):
        if not row_ids or len(row_ids) == 0:
            pass
        stmt = select(ProxyIpPool).where(
            ProxyIpPool.id.in_(row_ids),
            ProxyIpPool.status == 0,
        )
        return self.db.scalars(stmt).all()

    def find_by_ip_port_user_pwd(self, ip:str, port, user_name, pwd):
        stmt = select(ProxyIpPool).where(
            ProxyIpPool.ip == ip,
            ProxyIpPool.port == port,
            ProxyIpPool.user_name == user_name,
            ProxyIpPool.password == pwd,
            ProxyIpPool.status == 0
        )
        return self.db.scalars(stmt).first()
