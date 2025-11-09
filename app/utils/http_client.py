"""Безопасный HTTP-клиент с таймаутами и ретраями."""

import time

import httpx


class SecureHTTPClient:
    """HTTP-клиент с настройками безопасности: таймауты, ретраи, лимиты."""

    def __init__(
        self,
        connect_timeout: float = 3.0,
        read_timeout: float = 5.0,
        write_timeout: float = 5.0,
        max_retries: int = 3,
        retry_delay: float = 0.5,
    ):
        """
        Инициализация безопасного HTTP-клиента.

        Args:
            connect_timeout: Таймаут подключения в секундах
            read_timeout: Таймаут чтения в секундах
            write_timeout: Таймаут записи в секундах
            max_retries: Максимальное количество попыток
            retry_delay: Начальная задержка между попытками (exponential backoff)
        """
        self.timeout = httpx.Timeout(
            connect=connect_timeout,
            read=read_timeout,
            write=write_timeout,
            pool=5.0,  # Таймаут для пула соединений
        )
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def get(
        self,
        url: str,
        follow_redirects: bool = True,
        **kwargs,
    ) -> httpx.Response:
        """
        Выполняет GET запрос с ретраями и таймаутами.

        Args:
            url: URL для запроса
            follow_redirects: Следовать ли редиректам
            **kwargs: Дополнительные параметры для httpx

        Returns:
            httpx.Response объект

        Raises:
            httpx.HTTPError: если все попытки неудачны
        """
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                with httpx.Client(
                    timeout=self.timeout,
                    follow_redirects=follow_redirects,
                ) as client:
                    response = client.get(url, **kwargs)
                    response.raise_for_status()
                    return response
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    delay = self.retry_delay * (2**attempt)
                    time.sleep(delay)
        # Все попытки исчерпаны
        raise httpx.HTTPError("Max retries exceeded") from last_exception

    def post(
        self,
        url: str,
        follow_redirects: bool = True,
        **kwargs,
    ) -> httpx.Response:
        """
        Выполняет POST запрос с ретраями и таймаутами.

        Args:
            url: URL для запроса
            follow_redirects: Следовать ли редиректам
            **kwargs: Дополнительные параметры для httpx

        Returns:
            httpx.Response объект

        Raises:
            httpx.HTTPError: если все попытки неудачны
        """
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                with httpx.Client(
                    timeout=self.timeout,
                    follow_redirects=follow_redirects,
                ) as client:
                    response = client.post(url, **kwargs)
                    response.raise_for_status()
                    return response
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    delay = self.retry_delay * (2**attempt)
                    time.sleep(delay)
        # Все попытки исчерпаны
        raise httpx.HTTPError("Max retries exceeded") from last_exception


# Глобальный экземпляр с безопасными настройками по умолчанию
default_client = SecureHTTPClient()
