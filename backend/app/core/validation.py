"""Request validation error message helpers."""

from __future__ import annotations

from typing import Any

from fastapi.exceptions import RequestValidationError

FIELD_LABELS: dict[str, str] = {
    "name": "姓名",
    "age": "年龄",
    "code": "演员编码",
    "stage_name": "艺名",
    "tags": "标签",
    "bio": "简介",
    "gender": "性别",
    "username": "用户名",
    "password": "密码",
    "title": "标题",
    "director": "导演",
    "genre": "类型",
}


def _field_label(loc: list[Any]) -> str:
    parts = [str(x) for x in loc if x not in ("body", "query", "path", "header")]
    field = parts[-1] if parts else "参数"
    return FIELD_LABELS.get(field, field)


def format_validation_message(exc: RequestValidationError) -> str:
    """Convert Pydantic validation errors into a single Chinese message."""
    errors = exc.errors()
    if not errors:
        return "参数校验失败"

    err = errors[0]
    label = _field_label(list(err.get("loc") or []))
    err_type = err.get("type") or ""
    ctx = err.get("ctx") or {}

    if err_type == "string_too_long":
        return f"{label}不能超过{ctx.get('max_length')}个字符"
    if err_type == "string_too_short":
        return f"{label}不能少于{ctx.get('min_length')}个字符"
    if err_type == "missing":
        return f"{label}不能为空"
    if err_type in {
        "int_parsing",
        "int_type",
        "float_parsing",
        "float_type",
        "bool_parsing",
        "bool_type",
    }:
        return f"{label}格式不正确"
    if err_type == "greater_than_equal":
        return f"{label}不能小于{ctx.get('ge')}"
    if err_type == "less_than_equal":
        return f"{label}不能大于{ctx.get('le')}"
    if err_type == "greater_than":
        return f"{label}必须大于{ctx.get('gt')}"
    if err_type == "less_than":
        return f"{label}必须小于{ctx.get('lt')}"
    if err_type == "string_type":
        return f"{label}必须是字符串"
    if err_type == "value_error":
        msg = err.get("msg") or "参数不正确"
        return f"{label}{msg}" if label != "参数" else msg

    return f"{label}参数不正确"
