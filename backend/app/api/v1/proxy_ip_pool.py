"""Proxy IP pool endpoints (sync)."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_proxy_ip_pool_service
from app.core.response import ApiResponse, success
from app.schemas.common import PageData
from app.schemas.proxy_ip_pool import ProxyIpPoolCreate, ProxyIpPoolOut, ProxyIpPoolUpdate
from app.services.proxy_ip_pool_service import ProxyIpPoolService

router = APIRouter()


@router.post("/create", response_model=ApiResponse[bool], summary="Create proxy IP")
def create_proxy_ip(
    req: ProxyIpPoolCreate,
    service: Annotated[ProxyIpPoolService, Depends(get_proxy_ip_pool_service)],
) -> ApiResponse[bool]:
    return success(service.create(req))


@router.post("/update", response_model=ApiResponse[bool], summary="Update proxy IP")
def update_proxy_ip(
    req: ProxyIpPoolUpdate,
    service: Annotated[ProxyIpPoolService, Depends(get_proxy_ip_pool_service)],
) -> ApiResponse[bool]:
    return success(service.update(req))


@router.get("/find_by_id", response_model=ApiResponse[ProxyIpPoolOut], summary="Find proxy IP")
def find_by_id(
    service: Annotated[ProxyIpPoolService, Depends(get_proxy_ip_pool_service)],
    id: int = Query(..., description="主键"),
) -> ApiResponse[ProxyIpPoolOut]:
    return success(service.find_by_id(id))


@router.get("/delete_by_id", response_model=ApiResponse[bool], summary="Delete proxy IP")
def delete_by_id(
    service: Annotated[ProxyIpPoolService, Depends(get_proxy_ip_pool_service)],
    id: int = Query(..., description="主键"),
) -> ApiResponse[bool]:
    return success(service.delete_by_id(id))


@router.get("/page_list", response_model=ApiResponse[PageData[ProxyIpPoolOut]], summary="Page proxy IP")
def page_list(
    service: Annotated[ProxyIpPoolService, Depends(get_proxy_ip_pool_service)],
    page_no: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    keyword: Optional[str] = Query(default=None, description="IP/城市/备注模糊"),
    usage_status: Optional[bool] = Query(default=None, description="是否可用"),
) -> ApiResponse[PageData[ProxyIpPoolOut]]:
    data = service.page_list(page_no, page_size, keyword=keyword, usage_status=usage_status)
    return success(data)
