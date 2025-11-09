"""Тесты для безопасной работы с секретами."""

import os
from unittest.mock import patch

import pytest

from app.utils.secrets import SecretManager


def test_get_secret_exists():
    """Позитивный тест: получение существующего секрета"""
    with patch.dict(os.environ, {"TEST_SECRET": "test_value"}):
        value = SecretManager.get_secret("TEST_SECRET")
        assert value == "test_value"


def test_get_secret_not_exists():
    """Тест: получение несуществующего секрета"""
    with patch.dict(os.environ, {}, clear=True):
        value = SecretManager.get_secret("NONEXISTENT_SECRET")
        assert value is None


def test_get_secret_with_default():
    """Тест: получение секрета с default значением"""
    with patch.dict(os.environ, {}, clear=True):
        value = SecretManager.get_secret("NONEXISTENT_SECRET", default="default_value")
        assert value == "default_value"


def test_get_secret_required_exists():
    """Позитивный тест: получение обязательного секрета"""
    with patch.dict(os.environ, {"REQUIRED_SECRET": "required_value"}):
        value = SecretManager.get_secret_required("REQUIRED_SECRET")
        assert value == "required_value"


def test_get_secret_required_not_exists():
    """Негативный тест: обязательный секрет не найден"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Required secret"):
            SecretManager.get_secret_required("NONEXISTENT_SECRET")


def test_mask_secret_short():
    """Тест маскировки короткого секрета"""
    masked = SecretManager.mask_secret("abc", visible_chars=4)
    assert masked == "***"  # Все символы скрыты, т.к. длина <= visible_chars


def test_mask_secret_long():
    """Тест маскировки длинного секрета"""
    masked = SecretManager.mask_secret("my_secret_key_12345", visible_chars=4)
    assert masked.startswith("my_s")
    assert masked.endswith("****")
    assert len(masked) == len("my_secret_key_12345")


def test_mask_secret_default_visible():
    """Тест маскировки с дефолтным количеством видимых символов"""
    masked = SecretManager.mask_secret("very_long_secret_key")
    assert masked.startswith("very")
    assert masked.count("*") > 0


def test_secret_not_logged():
    """Негативный тест: секреты не должны логироваться"""
    with patch.dict(os.environ, {"API_KEY": "secret123"}):
        with patch("app.utils.secrets.logger") as mock_logger:
            SecretManager.get_secret("API_KEY")

            # Проверяем, что в логах нет значения секрета
            for call in mock_logger.debug.call_args_list:
                if call:
                    log_message = str(call)
                    assert "secret123" not in log_message
                    assert "value hidden" in log_message or "is set" in log_message
