"""Валидация и нормализация данных с использованием Decimal и UTC."""

import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_datetime_to_utc(dt: datetime) -> datetime:
    """
    Нормализует datetime к UTC и убирает timezone info.

    Args:
        dt: datetime объект (может быть с timezone или без)

    Returns:
        datetime в UTC без timezone info
    """
    if dt.tzinfo is None:
        # Если timezone нет, считаем что это UTC
        return dt.replace(tzinfo=timezone.utc).replace(tzinfo=None)
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


def parse_decimal_safe(value: Any) -> Decimal:
    """
    Безопасно парсит значение в Decimal, избегая float погрешностей.

    Args:
        value: значение для парсинга (str, int, float, Decimal)

    Returns:
        Decimal объект

    Raises:
        ValueError: если значение не может быть преобразовано в Decimal
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        try:
            return Decimal(value)
        except InvalidOperation:
            raise ValueError(f"Cannot convert '{value}' to Decimal")
    if isinstance(value, (int, float)):
        # Для float используем строковое представление для точности
        return Decimal(str(value))
    raise ValueError(f"Unsupported type for Decimal conversion: {type(value)}")


def parse_json_safe(raw_json: str, parse_float: type = str) -> dict:
    """
    Безопасно парсит JSON, избегая float погрешностей.

    Args:
        raw_json: JSON строка
        parse_float: функция для парсинга float (по умолчанию str для Decimal)

    Returns:
        dict с распарсенными данными
    """
    return json.loads(raw_json, parse_float=parse_float)


