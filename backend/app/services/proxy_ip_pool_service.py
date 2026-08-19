"""Proxy IP pool business logic."""

from __future__ import annotations

from typing import Optional


from app.client.resp.xiu_xiu_ip import XiuXiuOrder, XiuXiuDataInfo
from app.client.xiu_xiu_ip_client import query_ip_page, query_ip_info
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

    def query_by_ids(self,row_ids: list[int]) -> list[ProxyIpPoolOut]:
        self.repo.query_by_ids(row_ids)

    def find_by_ip_port_user_pwd(self,ip:str,port:int,user_name:str,pwd:str) -> ProxyIpPoolOut:
        return  self.repo.find_by_ip_port_user_pwd(ip, port,user_name,pwd)

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

    def ip_pool_sync(self) -> bool:
        page = 1
        page_size = 10
        total, ip_list = query_ip_page(page, page_size)
        if not total or total == 0:
            pass
        total_page = int(total / page_size + 1)

        ip_data_total:list[XiuXiuDataInfo] = []
        for index_page in range(1,total_page+1):
            order_list:list[XiuXiuOrder]
            _,order_list = query_ip_page(index_page, page_size)
            if not order_list:
                continue
            for item in order_list:
                order_id = item.iid
                data_info = query_ip_info(order_id)
                if data_info:
                    ip_data_total.append(data_info)
        if not ip_data_total:
            return  True

        for item in ip_data_total:
            ip = item.ip
            port = item.socks_http.split("/")[1]
            user_name = item.username
            password = item.password
            city = item.city
            ip_exist = self.find_by_ip_port_user_pwd(ip,port,user_name,password)
            if(ip_exist):
                #更新
                exist_id = ip_exist.id
                pass
            else :
                #新增
                save = ProxyIpPoolCreate()
                save.ip = ip
                save.port = port
                save.user_name = user_name
                save.password = password
                save.city = city
                self.create(save)
                pass




