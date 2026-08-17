"""Proxy IP pool ORM model — table proxy_ip_pool."""

from datetime import datetime

from sqlalchemy import Boolean, String, func, text
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProxyIpPool(Base):
    """代理 IP 池。"""

    __tablename__ = "proxy_ip_pool"

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="主键",
    )
    ip: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="代理IP",
    )
    port: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("'0'"),
        comment="代理端口",
    )
    city: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="城市",
    )
    user_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="代理用户名",
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        server_default=text("''"),
        comment="代理密码",
    )
    usage_status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("1"),
        comment="是否可用 0否 1是",
    )
    remark: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="备注",
    )
    status: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        default=0,
        server_default=text("0"),
        comment="删除标志 0未删除 1已删除",
    )
    create_time: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        comment="创建时间",
    )
    update_time: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
        comment="最后修改时间",
    )
