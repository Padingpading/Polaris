"""Request validation error message helpers."""

from __future__ import annotations

import json
from typing import Any

from fastapi.exceptions import RequestValidationError

# 字段中文名
FIELD_LABELS: dict[str, str] = {
    "name": "姓名",
    "age": "年龄",
    "code": "演员编码",
    "stage_name": "艺名",
    "tags": "标签",
    "bio": "简介",
    "gender": "性别",
    "is_active": "启用状态",
    "fan_count": "粉丝数",
    "view_count": "浏览量",
    "height_cm": "身高",
    "rating": "评分",
    "birth_date": "出生日期",
    "debut_time": "出道时间",
    "last_login_at": "最近登录时间",
    "username": "用户名",
    "password": "密码",
    "email": "邮箱",
    "full_name": "姓名",
    "title": "标题",
    "director": "导演",
    "genre": "类型",
    "release_year": "上映年份",
    "duration_minutes": "时长",
    "page": "页码",
    "page_size": "每页条数",
}

# 字段 + 错误类型 -> 具体中文文案（可用 {le}/{ge}/{min_length}/{max_length} 等）
FIELD_RULE_MESSAGES: dict[tuple[str, str], str] = {
    # actor
    ("age", "less_than_equal"): "年龄不能超过{le}岁，当前输入为无效年龄",
    ("age", "greater_than_equal"): "年龄不能小于{ge}岁",
    ("age", "int_parsing"): "年龄必须填写整数，例如 18",
    ("age", "int_type"): "年龄必须填写整数，例如 18",
    ("age", "missing"): "请填写年龄",
    ("fan_count", "missing"): "请填写粉丝数",
    ("fan_count", "int_parsing"): "粉丝数必须填写整数",
    ("fan_count", "int_type"): "粉丝数必须填写整数",
    ("view_count", "missing"): "请填写浏览量",
    ("view_count", "int_parsing"): "浏览量必须填写整数",
    ("view_count", "int_type"): "浏览量必须填写整数",
    ("name", "missing"): "请填写姓名",
    ("name", "string_too_short"): "姓名至少需要{min_length}个字符",
    ("name", "string_too_long"): "姓名最多{max_length}个字符",
    ("name", "string_type"): "姓名必须是文字内容",
    ("stage_name", "string_too_long"): "艺名最多{max_length}个字符",
    ("code", "missing"): "请填写演员编码",
    ("code", "string_too_short"): "演员编码至少{min_length}位",
    ("code", "string_too_long"): "演员编码最多{max_length}位",
    ("gender", "less_than_equal"): "性别取值无效，请传 0-3",
    ("gender", "greater_than_equal"): "性别取值无效，请传 0-3",
    # user / auth
    ("username", "missing"): "请填写用户名",
    ("username", "string_too_short"): "用户名至少{min_length}位",
    ("username", "string_too_long"): "用户名最多{max_length}位",
    ("password", "missing"): "请填写密码",
    ("password", "string_too_short"): "密码至少{min_length}位",
    ("password", "string_too_long"): "密码最多{max_length}位",
    ("email", "missing"): "请填写邮箱",
    # movie
    ("title", "missing"): "请填写影片标题",
    ("title", "string_too_short"): "影片标题不能为空",
    ("title", "string_too_long"): "影片标题最多{max_length}个字符",
    ("release_year", "greater_than_equal"): "上映年份不能早于{ge}年",
    ("release_year", "less_than_equal"): "上映年份不能晚于{le}年",
    ("rating", "greater_than_equal"): "评分不能低于{ge}",
    ("rating", "less_than_equal"): "评分不能高于{le}",
    # paging
    ("page", "greater_than_equal"): "页码从{ge}开始",
    ("page_size", "less_than_equal"): "每页最多查询{le}条",
    ("page_size", "greater_than_equal"): "每页至少查询{ge}条",
}


def _field_name(loc: list[Any]) -> str:
    parts = [str(x) for x in loc if x not in ("body", "query", "path", "header")]
    return parts[-1] if parts else "参数"


def _field_label(loc: list[Any]) -> str:
    field = _field_name(loc)
    return FIELD_LABELS.get(field, field)


def _format_template(template: str, ctx: dict[str, Any]) -> str:
    try:
        return template.format(**ctx)
    except Exception:
        return template


def _translate_one(err: dict[str, Any]) -> str:
    loc = list(err.get("loc") or [])
    field = _field_name(loc)
    label = _field_label(loc)
    err_type = err.get("type") or ""
    ctx = dict(err.get("ctx") or {})

    specific = FIELD_RULE_MESSAGES.get((field, err_type))
    if specific:
        return _format_template(specific, ctx)

    # 通用兜底文案
    if err_type == "string_too_long":
        return f"{label}最多只能输入{ctx.get('max_length')}个字符"
    if err_type == "string_too_short":
        return f"{label}至少需要输入{ctx.get('min_length')}个字符"
    if err_type == "missing":
        return f"请填写{label}"
    if err_type in {
        "int_parsing",
        "int_type",
        "float_parsing",
        "float_type",
        "bool_parsing",
        "bool_type",
        "decimal_parsing",
        "decimal_type",
    }:
        return f"{label}格式不正确，请按要求重新填写"
    if err_type == "greater_than_equal":
        return f"{label}不能小于{ctx.get('ge')}"
    if err_type == "less_than_equal":
        return f"{label}不能大于{ctx.get('le')}"
    if err_type == "greater_than":
        return f"{label}必须大于{ctx.get('gt')}"
    if err_type == "less_than":
        return f"{label}必须小于{ctx.get('lt')}"
    if err_type == "string_type":
        return f"{label}必须是文字内容"
    if err_type == "list_type":
        return f"{label}必须是列表"
    if err_type == "value_error":
        msg = err.get("msg") or "填写不正确"
        if isinstance(msg, str) and msg.startswith("Value error, "):
            msg = msg.removeprefix("Value error, ")
        return f"{label}{msg}" if not str(msg).startswith(label) else str(msg)

    return f"{label}填写不正确，请检查后重试"


def format_validation_message(exc: RequestValidationError) -> str:
    """Convert Pydantic validation errors into a single Chinese message."""
    errors = exc.errors()
    if not errors:
        return "参数校验失败，请检查提交内容"
    return _translate_one(errors[0])


def format_validation_errors(exc: RequestValidationError) -> list[dict[str, Any]]:
    """Return validation errors with Chinese msg for API data."""
    result: list[dict[str, Any]] = []
    for err in exc.errors():
        result.append(
            {
                "field": _field_label(list(err.get("loc") or [])),
                "type": err.get("type"),
                "msg": _translate_one(err),
                "input": err.get("input"),
            }
        )
    return result
