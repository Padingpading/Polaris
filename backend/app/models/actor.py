"""Actor ORM model — aligned with java-agents-style 数据库Mysql rules."""

from datetime import date, datetime, time
from decimal import Decimal
from enum import IntEnum
from typing import Optional

import sqlalchemy
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Index,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ActorGender(IntEnum):
    """性别: tinyint 枚举值。"""

    UNKNOWN = 0
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Actor(Base):
    """演员练习表（插件 数据库Mysql 规范）。"""
    __tablename__ = "actors"
    # __table_args__ = (
    #     UniqueConstraint("code", name="udx_code"),
    #     Index("idx_name", "name"),
    #     Index("idx_is_active_gender", "is_active", "gender"),
    #     {
    #         "mysql_engine": "InnoDB",
    #         "mysql_charset": "utf8mb4",
    #         "mysql_collate": "utf8mb4_bin",
    #         "mysql_row_format": "DYNAMIC",
    #         "comment": "演员练习表",
    #     },
    # )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="主键",
    )
    code: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default=text("''"),
        comment="演员编码",
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="真实姓名",
    )
    stage_name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("''"),
        comment="艺名",
    )
    tags: Mapped[str] = mapped_column(
        String(4080),
        nullable=False,
        server_default=text("''"),
        comment="标签JSON（截断存储）",
    )
    bio: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="简介",
    )
    gender: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        default=int(ActorGender.UNKNOWN),
        server_default=text("0"),
        comment="性别:0未知1男2女3其他",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("1"),
        comment="是否启用",
    )
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
        comment="年龄",
    )
    fan_count: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default=text("0"),
        comment="粉丝数",
    )
    view_count: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        nullable=False,
        server_default=text("0"),
        comment="浏览量",
    )
    height_cm: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        server_default=text("0.00"),
        comment="身高厘米",
    )
    rating: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        server_default=text("0.00"),
        comment="评分",
    )
    birth_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, comment="出生日期"
    )
    debut_time: Mapped[Optional[time]] = mapped_column(
        Time, nullable=True, comment="出道时间点"
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="最近登录时间"
    )
    status: Mapped[int] = mapped_column(
        TINYINT(unsigned=True),
        nullable=False,
        server_default=text("0"),
        comment="状态",
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


