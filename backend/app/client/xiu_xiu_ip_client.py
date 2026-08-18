"""XiuXiu IP / order HTTP client."""

from __future__ import annotations

import requests

from app.client.resp.xiu_xiu_ip import XiuXiuOrder

_BASE_URL = "https://www.niuniukj.com:11222/api/v1/homeJ/listSearchOrder"
_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxOTk1MDA3MTM0NiIsInRpbWUiOiIyMDI2LTA2LTIyIDE2OjUzOjEzIiwiaXAiOiI1OC4yNDcuMTQzLjQyIiwiZXhwIjoxODA4MDM4MzkzfQ."
    "SE5kh4M4H6363RYe_XhLMlOeN4L2duP_qnkCa0FZeZ0"
)


def query_ip_page(page_no: int, page_size: int) -> tuple[int, list[XiuXiuOrder]]:
    url = f"{_BASE_URL}?page={page_no}&size={page_size}"
    resp = requests.get(
        url=url,
        headers={"Authorization": f"Bearer {_TOKEN}"},
        timeout=30,
    )
    resp.raise_for_status()
    rows = resp.json().get("data", {}).get("rows") or []
    total = resp.json().get("total", 0)
    return (total, [XiuXiuOrder(**item) for item in rows])

