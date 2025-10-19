from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100


def test_upload_ok_png(tmp_path):
    files = {"file": ("x.png", PNG, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True and body.get("path")


def test_upload_too_big(tmp_path):
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (5_000_001)
    files = {"file": ("big.png", big, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 413
    assert r.json().get("status") == 413


def test_upload_bad_type(tmp_path):
    bad = b"not_an_image"
    files = {"file": ("x.png", bad, "application/octet-stream")}
    r = client.post("/upload", files=files)
    assert r.status_code == 400
    assert r.json().get("title") == "Bad Request"
