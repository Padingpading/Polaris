"""Proxy IP pool request/response schemas."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.schemas.common import str_length


class ProxyIpPoolCreate(BaseModel):
    """Create proxy IP."""

    ip: Annotated[str, Field(default=...), str_length(1, 64, "IP长度须在1~64个字符之间")]
    port: Annotated[str, Field(default="0"), str_length(0, 64, "端口最多64个字符")]
    city: Annotated[str, Field(default=""), str_length(0, 64, "城市最多64个字符")]
    user_name: Annotated[str, Field(default=""), str_length(0, 64, "用户名最多64个字符")]
    password: Annotated[str, Field(default=""), str_length(0, 128, "密码最多128个字符")]
    usage_status: bool = True
    remark: Annotated[str, Field(default=""), str_length(0, 64, "备注最多64个字符")]


class ProxyIpPoolUpdate(BaseModel):
    """Update proxy IP."""

    id: int = Field(default=..., description="主键")
    ip: Annotated[str, Field(default=...), str_length(1, 64, "IP长度须在1~64个字符之间")]
    port: Annotated[str, Field(default="0"), str_length(0, 64, "端口最多64个字符")]
    city: Annotated[str, Field(default=""), str_length(0, 64, "城市最多64个字符")]
    user_name: Annotated[str, Field(default=""), str_length(0, 64, "用户名最多64个字符")]
    password: Annotated[str, Field(default=""), str_length(0, 128, "密码最多128个字符")]
    usage_status: bool = True
    remark: Annotated[str, Field(default=""), str_length(0, 64, "备注最多64个字符")]


class ProxyIpPoolOut(BaseModel):
    """Proxy IP response."""

    id: int
    ip: str
    port: str
    city: str
    user_name: str
    password: str
    usage_status: bool
    remark: str
    status: int
    create_time: datetime
    update_time: datetime

    model_config = {"from_attributes": True}
