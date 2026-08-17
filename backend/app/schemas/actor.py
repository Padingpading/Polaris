"""Actor request/response schemas."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from app.schemas.common import int_range, str_length


class ActorCreate(BaseModel):
    """Create actor request."""

    name: Annotated[
        str,
        Field(default=...),
        str_length(1, 64, "姓名长度须在1~64个字符之间"),
    ]
    stage_name: Annotated[
        str,
        Field(default=""),
        str_length(0, 64, "艺名最多64个字符"),
    ]
    age: Annotated[
        int,
        Field(default=0),
        int_range(0, 150, "年龄必须在0~150岁之间，请填写真实年龄"),
    ]
    fan_count: Annotated[
        int,
        Field(default=0),
        int_range(0, 9_000_000_000, "粉丝数必须为大于等于0的整数"),
    ]
    view_count: Annotated[
        int,
        Field(default=0),
        int_range(0, 9_000_000_000, "浏览量必须为大于等于0的整数"),
    ]
    tags: str = ""
    bio: Annotated[
        str,
        Field(default=""),
        str_length(0, 200, "简介的字数最大是200"),
    ]
    gender_desc: str = ""
    height_cm: float = 0.0
    rating: float = 0.0
    debut_time: str = ""
    birth_date: str = ""


class ActorUpdate(BaseModel):
    """Update actor request."""

    code: Annotated[
        str,
        Field(default=...),
        str_length(1, 32, "演员编码不能为空"),
    ]
    name: Annotated[
        str,
        Field(default=...),
        str_length(1, 64, "姓名长度须在1~64个字符之间"),
    ]
    stage_name: Annotated[
        str,
        Field(default=""),
        str_length(0, 64, "艺名最多64个字符"),
    ]
    age: Annotated[
        int,
        Field(default=0),
        int_range(0, 150, "年龄必须在0~150岁之间，请填写真实年龄"),
    ]
    fan_count: Annotated[
        int,
        Field(default=0),
        int_range(0, 9_000_000_000, "粉丝数必须为大于等于0的整数"),
    ]
    view_count: Annotated[
        int,
        Field(default=0),
        int_range(0, 9_000_000_000, "浏览量必须为大于等于0的整数"),
    ]
    tags: str = ""
    bio: Annotated[
        str,
        Field(default=""),
        str_length(0, 200, "简介的字数最大是200"),
    ]
    gender_desc: str = ""
    height_cm: float = 0.0
    rating: float = 0.0
    debut_time: str = ""
    birth_date: str = ""


class ActorOut(BaseModel):
    """Actor response."""
    id: int
    code: str
    name: str
    stage_name: str
    tags: str
    bio: str
    gender: int
    is_active: bool
    age: int
    fan_count: int
    view_count: int
    height_cm: Decimal
    rating: Decimal
    birth_date: Optional[date] = None
    debut_time: Optional[time] = None
    last_login_at: Optional[datetime] = None
    create_time: datetime
    update_time: datetime

    model_config = {"from_attributes": True}
