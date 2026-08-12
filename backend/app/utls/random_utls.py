"""ID helpers: UUID and Snowflake."""

from __future__ import annotations

import threading
import time
from uuid import uuid4


def uuid() -> str:
    """Return UUID4 string without hyphens."""
    return str(uuid4()).replace("-", "")


class _Snowflake:
    """Simple 64-bit snowflake: 41 time + 5 dc + 5 worker + 12 seq."""

    def __init__(self, datacenter_id: int = 1, worker_id: int = 1) -> None:
        self.datacenter_id = datacenter_id & 0x1F
        self.worker_id = worker_id & 0x1F
        self.sequence = 0
        self.last_ts = -1
        self.lock = threading.Lock()
        self.epoch = 1704067200000  # 2024-01-01 UTC

    def _ts(self) -> int:
        return int(time.time() * 1000)

    def next_id(self) -> int:
        with self.lock:
            ts = self._ts()
            if ts < self.last_ts:
                raise RuntimeError("clock moved backwards")
            if ts == self.last_ts:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    while ts <= self.last_ts:
                        ts = self._ts()
            else:
                self.sequence = 0
            self.last_ts = ts
            return (
                ((ts - self.epoch) << 22)
                | (self.datacenter_id << 17)
                | (self.worker_id << 12)
                | self.sequence
            )


_snowflake = _Snowflake()


def snowflake_id() -> str:
    """Return snowflake id as string."""
    return str(_snowflake.next_id())
