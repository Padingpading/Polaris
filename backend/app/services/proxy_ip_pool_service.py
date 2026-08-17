"""Proxy IP pool business logic."""

from __future__ import annotations

from typing import Optional

from app.core.exceptions import AppException
from app.models.proxy_ip_pool import ProxyIpPool
from app.repositories.proxy_ip_pool_repository import ProxyIpPoolRepository
from app.schemas.common import PageData
from app.schemas.proxy_ip_pool import ProxyIpPoolCreate, ProxyIpPoolOut, ProxyIpPoolUpdate


class ProxyIpPoolService:
    """Proxy IP pool CRUD operations."""

    def __init__(self, repo: ProxyIpPoolRepository) -> None:
        self.repo = repo

    def create(self, payload: ProxyIpPoolCreate) -> bool:
        row = ProxyIpPool(
            ip=payload.ip,
            port=payload.port,
            city=payload.city,
            user_name=payload.user_name,
            password=payload.password,
            usage_status=payload.usage_status,
            remark=payload.remark,
            status=0,
        )
        self.repo.save(row)
        return True

    def update(self, payload: ProxyIpPoolUpdate) -> bool:
        row = self.repo.find_by_id(payload.id)
        if row is None:
            raise AppException("未查询到代理IP信息")
        ok = self.repo.update_by_id(
            payload.id,
            ip=payload.ip,
            port=payload.port,
            city=payload.city,
            user_name=payload.user_name,
            password=payload.password,
            usage_status=payload.usage_status,
            remark=payload.remark,
        )
        if not ok:
            raise AppException("更新失败")
        return True

    def find_by_id(self, row_id: int) -> ProxyIpPoolOut:
        row = self.repo.find_by_id(row_id)
        if row is None:
            raise AppException("未查询到代理IP信息")
        return ProxyIpPoolOut.model_validate(row)

    def delete_by_id(self, row_id: int) -> bool:
        ok = self.repo.delete_by_id(row_id)
        if not ok:
            raise AppException("未查询到代理IP信息或删除失败")
        return True

    def page_list(
        self,
        page_no: int,
        page_size: int,
        keyword: Optional[str] = None,
        usage_status: Optional[bool] = None,
    ) -> PageData[ProxyIpPoolOut]:
        offset = (page_no - 1) * page_size
        items, total = self.repo.page_list(
            keyword=keyword,
            usage_status=usage_status,
            offset=offset,
            limit=page_size,
        )
        return PageData(
            items=[ProxyIpPoolOut.model_validate(item) for item in items],
            total=total,
            page=page_no,
            page_size=page_size,
        )
