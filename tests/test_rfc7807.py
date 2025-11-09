"""Тесты для RFC 7807 формата ошибок на всех эндпойнтах."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_deck_not_found_rfc7807():
    """Тест: ошибка 404 для несуществующей колоды в формате RFC 7807"""
    r = client.get("/decks/99999")
    assert r.status_code == 404
    body = r.json()

    # Проверяем RFC 7807 формат
    assert body.get("type") == "about:blank"
    assert body.get("title") == "Not Found"
    assert body.get("status") == 404
    assert body.get("detail") == "deck not found"
    assert "correlation_id" in body
    assert body.get("code") == "deck_not_found"

    # Проверяем Content-Type
    assert r.headers.get("content-type") == "application/problem+json"


def test_card_not_found_rfc7807():
    """Тест: ошибка 404 для несуществующей карточки в формате RFC 7807"""
    r = client.get("/cards/99999")
    assert r.status_code == 404
    body = r.json()

    # Проверяем RFC 7807 формат
    assert body.get("type") == "about:blank"
    assert body.get("title") == "Not Found"
    assert body.get("status") == 404
    assert body.get("detail") == "card not found"
    assert "correlation_id" in body
    assert body.get("code") == "card_not_found"


def test_card_deck_not_found_rfc7807(test_db):
    """Тест: ошибка 404 при создании карточки для несуществующей колоды"""
    r = client.post(
        "/cards",
        json={"deck_id": 99999, "front": "test", "back": "test"},
    )
    assert r.status_code == 404
    body = r.json()

    # Проверяем RFC 7807 формат
    assert body.get("type") == "about:blank"
    assert body.get("title") == "Not Found"
    assert body.get("status") == 404
    assert body.get("detail") == "deck not found"
    assert "correlation_id" in body
    assert body.get("code") == "deck_not_found"


def test_upload_error_rfc7807():
    """Тест: ошибка загрузки в формате RFC 7807"""
    bad = b"not_an_image"
    files = {"file": ("x.png", bad, "application/octet-stream")}
    r = client.post("/upload", files=files)
    assert r.status_code == 400
    body = r.json()

    # Проверяем RFC 7807 формат
    assert body.get("type") == "about:blank"
    assert body.get("title") == "Bad Request"
    assert body.get("status") == 400
    assert "correlation_id" in body
    assert body.get("code") == "bad_type"


def test_upload_too_big_rfc7807():
    """Тест: ошибка превышения размера в формате RFC 7807"""
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (5_000_001)
    files = {"file": ("big.png", big, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 413
    body = r.json()

    # Проверяем RFC 7807 формат
    assert body.get("type") == "about:blank"
    assert body.get("title") == "Payload Too Large"
    assert body.get("status") == 413
    assert "correlation_id" in body
    assert body.get("code") == "too_big"


def test_correlation_id_unique():
    """Тест: correlation_id уникален для каждого запроса"""
    r1 = client.get("/decks/99999")
    r2 = client.get("/decks/99998")

    body1 = r1.json()
    body2 = r2.json()

    # correlation_id должны быть разными
    assert body1.get("correlation_id") != body2.get("correlation_id")
    assert body1.get("correlation_id") is not None
    assert body2.get("correlation_id") is not None
