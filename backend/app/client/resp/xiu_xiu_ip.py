"""XiuXiu order response models."""

from __future__ import annotations

from typing import Any, Optional


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
    """秀秀 IP 详情（对接 dataInfo）。"""

    def __init__(
        self,
        username: Optional[str] = None,
        end_time: Optional[str] = None,
        game: Optional[str] = None,
        password: Optional[str] = None,
        nodes: Optional[list[Any]] = None,
        create_time: Optional[str] = None,
        node_count: Optional[int] = None,
        ip_userid: Optional[int] = None,
        node_type: Optional[str] = None,
        address_id: Optional[int] = None,
        game_id: Optional[int] = None,
        web_name: Optional[str] = None,
        uuid: Optional[str] = None,
        notice: Optional[str] = None,
        state: Optional[str] = None,
        ip_use: Optional[int] = None,
    ) -> None:
        self.username = username
        self.end_time = end_time
        self.game = game
        self.password = password
        self.nodes = nodes if nodes is not None else []
        self.create_time = create_time
        self.node_count = node_count
        self.ip_userid = ip_userid
        self.node_type = node_type
        self.address_id = address_id
        self.game_id = game_id
        self.web_name = web_name
        self.uuid = uuid
        self.notice = notice
        self.state = state
        self.ip_use = ip_use

