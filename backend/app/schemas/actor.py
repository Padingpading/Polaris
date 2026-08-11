"""Actor request/response schemas."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ActorCreate(BaseModel):
    """Create actor request."""

    # code: str = Field(..., min_length=1, max_length=32)
    # name: str = Field(..., min_length=1, max_length=64)
    # stage_name: str = Field(default="", max_length=64)
    # tags: str = Field(default="", max_length=4080)
    # bio: str = Field(default="")
    # gender: int = Field(default=0, ge=0, le=3)
    # is_active: bool = True
    age: int = Field(default=0, ge=0, le=150)
    # fan_count: int = Field(default=0, ge=0)
    # view_count: int = Field(default=0, ge=0)
    # height_cm: Decimal = Field(default=Decimal("0.00"))
    # rating: Decimal = Field(default=Decimal("0.00"))
    # birth_date: Optional[date] = None
    # debut_time: Optional[time] = None
    # last_login_at: Optional[datetime] = None
    #

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
