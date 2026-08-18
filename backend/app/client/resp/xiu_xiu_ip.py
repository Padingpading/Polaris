"""XiuXiu order response models."""

from typing import Optional


class XiuXiuOrder:
    """秀秀订单行（对接 listSearchOrder rows）。"""
    iid: str
    num: int
    game: str
    notes: Optional[str]
    node_type: str
    stoptime: str
    pid: Optional[str]
    refund: int
    ip_use: int


