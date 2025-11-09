"""Безопасная работа с секретами из окружения."""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class SecretManager:
    """Менеджер для безопасной работы с секретами."""

    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Получает секрет из переменных окружения.

        Args:
            key: Имя переменной окружения
            default: Значение по умолчанию, если переменная не найдена

        Returns:
            Значение секрета или default

        Warning:
            Никогда не логируйте значение секрета!
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"Secret '{key}' not found in environment")
        else:
            # Логируем только факт наличия, но не значение
            logger.debug(f"Secret '{key}' is set (value hidden)")
        return value

    @staticmethod
    def get_secret_required(key: str) -> str:
        """
        Получает обязательный секрет из переменных окружения.

        Args:
            key: Имя переменной окружения

        Returns:
            Значение секрета

        Raises:
            ValueError: если секрет не найден

        Warning:
            Никогда не логируйте значение секрета!
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Required secret '{key}' not found in environment")
        logger.debug(f"Required secret '{key}' is set (value hidden)")
        return value

    @staticmethod
    def mask_secret(value: str, visible_chars: int = 4) -> str:
        """
        Маскирует секрет для безопасного логирования.

        Args:
            value: Секрет для маскировки
            visible_chars: Количество видимых символов в начале

        Returns:
            Замаскированная строка (например, "abcd****")
        """
        if len(value) <= visible_chars:
            return "*" * len(value)
        return value[:visible_chars] + "*" * (len(value) - visible_chars)
