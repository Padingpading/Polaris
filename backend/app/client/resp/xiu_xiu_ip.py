"""XiuXiu order response models."""

from __future__ import annotations

from typing import Any, Optional


def _pick(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data.get(key) is not None:
            return data.get(key)
    return None


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int(value)


class XiuXiuOrder:
    """秀秀订单行（对接 listSearchOrder rows）。"""

    def __init__(
        self,
        iid: str,
        num: int,
        game: str,
        notes: Optional[str],
        node_type: str,
        stoptime: str,
        pid: Optional[str],
        refund: int,
        ip_use: int,
    ) -> None:
        self.iid = iid
        self.num = num
        self.game = game
        self.notes = notes
        self.node_type = node_type
        self.stoptime = stoptime
        self.pid = pid
        self.refund = refund
        self.ip_use = ip_use

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> XiuXiuOrder:
        """把接口返回的 dict 转成对象。"""
        return cls(
            iid=str(data.get("iid") or ""),
            num=int(data.get("num") or 0),
            game=str(data.get("game") or ""),
            notes=data.get("notes"),
            node_type=str(data.get("node_type") or ""),
            stoptime=str(data.get("stoptime") or ""),
            pid=data.get("pid") if data.get("pid") is not None else None,
            refund=int(data.get("refund") or 0),
            ip_use=int(data.get("ip_use") or 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "iid": self.iid,
            "num": self.num,
            "game": self.game,
            "notes": self.notes,
            "node_type": self.node_type,
            "stoptime": self.stoptime,
            "pid": self.pid,
            "refund": self.refund,
            "ip_use": self.ip_use,
        }


class XiuXiuDataInfo:
    """秀秀 IP 详情行（对接 OrderDetail rows）。"""

    def __init__(
        self,
        id: Optional[int] = None,
        ip: Optional[str] = None,
        ip_export: Optional[str] = None,
        is_use: Optional[int] = None,
        location: Optional[str] = None,
        city: Optional[str] = None,
        records: Optional[list[Any]] = None,
        socks_http: Optional[str] = None,
        update_count: Optional[int] = None,
        update_time: Optional[str] = None,
        isp: Optional[str] = None,
        checked: Optional[str] = None,
        days_left: Optional[int] = None,
        refund: Optional[int] = None,
        cus_username: Optional[str] = None,
        cus_password: Optional[str] = None,
        cus_port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        expire_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> None:
        self.id = id
        self.ip = ip
        self.ip_export = ip_export
        self.is_use = is_use
        self.location = location
        self.city = city
        self.records = records if records is not None else []
        self.socks_http = socks_http
        self.update_count = update_count
        self.update_time = update_time
        self.isp = isp
        self.checked = checked
        self.days_left = days_left
        self.refund = refund
        self.cus_username = cus_username
        self.cus_password = cus_password
        self.cus_port = cus_port
        self.username = username
        self.password = password
        self.expire_time = expire_time
        self.end_time = end_time

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> XiuXiuDataInfo:
        """把接口返回的 dict 转成对象（兼容 snake_case / camelCase）。"""
        if not data:
            return cls()
        records = _pick(data, "records")
        if records is None:
            records = []
        elif not isinstance(records, list):
            records = [records]
        return cls(
            id=_to_int(_pick(data, "id")),
            ip=_pick(data, "ip"),
            ip_export=_pick(data, "ipExport", "ip_export"),
            is_use=_to_int(_pick(data, "is_use", "isUse")),
            location=_pick(data, "location"),
            city=_pick(data, "city"),
            records=records,
            socks_http=_pick(data, "socksHttp", "socks_http"),
            update_count=_to_int(_pick(data, "updateCount", "update_count")),
            update_time=_pick(data, "updateTime", "update_time"),
            isp=_pick(data, "isp"),
            checked=_pick(data, "checked"),
            days_left=_to_int(_pick(data, "daysLeft", "days_left")),
            refund=_to_int(_pick(data, "refund")),
            cus_username=_pick(data, "cus_username", "cusUsername"),
            cus_password=_pick(data, "cus_password", "cusPassword"),
            cus_port=_to_int(_pick(data, "cus_port", "cusPort")),
            username=_pick(data, "username"),
            password=_pick(data, "password"),
            expire_time=_pick(data, "expire_time", "expireTime"),
            end_time=_pick(data, "end_time", "endTime"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ip": self.ip,
            "ipExport": self.ip_export,
            "is_use": self.is_use,
            "location": self.location,
            "city": self.city,
            "records": self.records,
            "socksHttp": self.socks_http,
            "updateCount": self.update_count,
            "updateTime": self.update_time,
            "isp": self.isp,
            "checked": self.checked,
            "daysLeft": self.days_left,
            "refund": self.refund,
            "cus_username": self.cus_username,
            "cus_password": self.cus_password,
            "cus_port": self.cus_port,
            "username": self.username,
            "password": self.password,
            "expire_time": self.expire_time,
            "end_time": self.end_time,
        }

