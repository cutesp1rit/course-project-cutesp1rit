"""Тесты для безопасного HTTP-клиента."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.utils.http_client import SecureHTTPClient


def test_http_client_initialization():
    """Тест инициализации HTTP-клиента с настройками"""
    client = SecureHTTPClient(
        connect_timeout=2.0,
        read_timeout=3.0,
        max_retries=2,
    )

    assert client.timeout.connect == 2.0
    assert client.timeout.read == 3.0
    assert client.max_retries == 2


def test_http_client_get_success():
    """Позитивный тест: успешный GET запрос"""
    client = SecureHTTPClient(max_retries=1)

    # Мокаем httpx.Client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get = MagicMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        response = client.get("https://httpbin.org/get")

        assert response.status_code == 200
        mock_client.get.assert_called_once()


def test_http_client_get_timeout():
    """Негативный тест: таймаут при GET запросе"""
    client = SecureHTTPClient(
        connect_timeout=0.001,  # Очень короткий таймаут
        read_timeout=0.001,
        max_retries=1,
    )

    with pytest.raises(httpx.HTTPError):
        # Попытка подключиться к несуществующему домену с коротким таймаутом
        client.get("https://192.0.2.1/", timeout=0.001)


def test_http_client_get_retry_on_failure():
    """Тест ретраев при неудачном запросе"""
    client = SecureHTTPClient(max_retries=3, retry_delay=0.1)

    call_count = 0

    def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.HTTPError("Connection error")
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        return mock_response

    with patch("httpx.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get = mock_get
        mock_client_class.return_value = mock_client

        with patch("time.sleep"):  # Ускоряем тест
            client.get("https://example.com")

        assert call_count == 3  # Должно быть 3 попытки


def test_http_client_get_max_retries_exceeded():
    """Негативный тест: превышение максимального количества ретраев"""
    client = SecureHTTPClient(max_retries=2, retry_delay=0.1)

    with patch("httpx.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get = MagicMock(side_effect=httpx.HTTPError("Connection error"))
        mock_client_class.return_value = mock_client

        with patch("time.sleep"):  # Ускоряем тест
            with pytest.raises(httpx.HTTPError, match="Max retries exceeded"):
                client.get("https://example.com")


def test_http_client_post_success():
    """Позитивный тест: успешный POST запрос"""
    client = SecureHTTPClient(max_retries=1)

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post = MagicMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        response = client.post("https://httpbin.org/post", json={"test": "data"})

        assert response.status_code == 201
        mock_client.post.assert_called_once()


def test_http_client_exponential_backoff():
    """Тест exponential backoff при ретраях"""
    client = SecureHTTPClient(max_retries=3, retry_delay=0.5)

    sleep_times = []

    def mock_sleep(seconds):
        sleep_times.append(seconds)

    with patch("httpx.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get = MagicMock(side_effect=httpx.HTTPError("Error"))
        mock_client_class.return_value = mock_client

        with patch("time.sleep", side_effect=mock_sleep):
            try:
                client.get("https://example.com")
            except httpx.HTTPError:
                pass

        # Проверяем exponential backoff: 0.5, 1.0, 2.0
        assert len(sleep_times) == 2  # 2 ретрая перед финальной ошибкой
        assert sleep_times[0] == 0.5  # Первая задержка
        assert sleep_times[1] == 1.0  # Вторая задержка (0.5 * 2^1)


