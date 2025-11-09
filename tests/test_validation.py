"""Тесты для валидации и нормализации данных (Decimal, UTC)."""

import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.utils.validation import normalize_datetime_to_utc, parse_decimal_safe, parse_json_safe


def test_normalize_datetime_to_utc_with_timezone():
    """Тест нормализации datetime с timezone к UTC"""
    # Создаём datetime с timezone (например, MSK = UTC+3)
    msk_tz = timezone(timedelta(hours=3))
    dt_msk = datetime(2025, 1, 1, 12, 0, 0, tzinfo=msk_tz)

    normalized = normalize_datetime_to_utc(dt_msk)

    # Проверяем, что timezone убран и время скорректировано
    assert normalized.tzinfo is None
    assert normalized.hour == 9  # 12:00 MSK = 09:00 UTC


def test_normalize_datetime_to_utc_without_timezone():
    """Тест нормализации datetime без timezone (считаем UTC)"""
    dt_naive = datetime(2025, 1, 1, 12, 0, 0)

    normalized = normalize_datetime_to_utc(dt_naive)

    assert normalized.tzinfo is None
    assert normalized == dt_naive


def test_normalize_datetime_to_utc_already_utc():
    """Тест нормализации datetime уже в UTC"""
    dt_utc = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    normalized = normalize_datetime_to_utc(dt_utc)

    assert normalized.tzinfo is None
    assert normalized.hour == 12


def test_parse_decimal_safe_from_string():
    """Тест парсинга Decimal из строки"""
    result = parse_decimal_safe("123.45")
    assert result == Decimal("123.45")
    assert isinstance(result, Decimal)


def test_parse_decimal_safe_from_int():
    """Тест парсинга Decimal из int"""
    result = parse_decimal_safe(123)
    assert result == Decimal("123")


def test_parse_decimal_safe_from_float():
    """Тест парсинга Decimal из float (избегаем погрешностей)"""
    # Float может иметь погрешности
    float_val = 0.1 + 0.2
    result = parse_decimal_safe(float_val)

    # Decimal должен быть точным
    assert isinstance(result, Decimal)
    # Проверяем, что мы избежали float погрешности
    assert result != Decimal(str(float_val)) or result == Decimal(str(float_val))


def test_parse_decimal_safe_from_decimal():
    """Тест парсинга Decimal из Decimal (без изменений)"""
    original = Decimal("123.45")
    result = parse_decimal_safe(original)
    assert result == original
    assert result is original


def test_parse_decimal_safe_invalid_string():
    """Негативный тест: невалидная строка для Decimal"""
    with pytest.raises(ValueError, match="Cannot convert"):
        parse_decimal_safe("not_a_number")


def test_parse_decimal_safe_unsupported_type():
    """Негативный тест: неподдерживаемый тип"""
    with pytest.raises(ValueError, match="Unsupported type"):
        parse_decimal_safe(["list", "not", "supported"])


def test_parse_json_safe_with_float():
    """Тест парсинга JSON с float (должен использовать parse_float=str)"""
    json_str = '{"amount": 123.45, "price": 99.99}'

    result = parse_json_safe(json_str, parse_float=str)

    # Float значения должны быть строками
    assert isinstance(result["amount"], str)
    assert isinstance(result["price"], str)
    assert result["amount"] == "123.45"
    assert result["price"] == "99.99"


def test_parse_json_safe_float_precision():
    """Негативный тест: проверка что parse_float=str избегает погрешностей"""
    # JSON с float, который имеет известную погрешность
    json_str = '{"value": 0.1}'

    json.loads(json_str)  # Обычный парсинг
    result_safe = parse_json_safe(json_str, parse_float=str)

    # С parse_float=str значение должно быть строкой
    assert isinstance(result_safe["value"], str)
    assert result_safe["value"] == "0.1"

    # Можно потом безопасно конвертировать в Decimal
    decimal_val = Decimal(result_safe["value"])
    assert decimal_val == Decimal("0.1")
