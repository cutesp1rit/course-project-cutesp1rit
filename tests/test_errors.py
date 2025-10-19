import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.nfr

client = TestClient(app)


def test_not_found_item():
    r = client.get("/items/999")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "not_found"


def test_validation_error():
    r = client.post("/items", params={"name": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["error"]["code"] == "validation_error"


def test_security_headers_present_on_ok_and_error():
    # OK response
    ok = client.get("/health")
    assert ok.status_code == 200
    for h, v in {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "X-XSS-Protection": "0",
    }.items():
        assert ok.headers.get(h) == v

    # Error response should also contain headers
    err = client.get("/items/999")
    assert err.status_code == 404
    for h, v in {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "X-XSS-Protection": "0",
    }.items():
        assert err.headers.get(h) == v


def test_body_size_limit_413():
    # Test upload endpoint with large file
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (5_000_001)
    files = {"file": ("big.png", big, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 413
    body = r.json()
    assert body.get("status") == 413
    assert body.get("title") == "Payload Too Large"
