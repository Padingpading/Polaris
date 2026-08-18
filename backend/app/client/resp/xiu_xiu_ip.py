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


xiu_xiu_order = XiuXiuOrder
