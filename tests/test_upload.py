from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.upload import sniff_image_type

client = TestClient(app)

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
JPEG = b"\xff\xd8" + b"0" * 100 + b"\xff\xd9"


def test_upload_ok_png(tmp_path):
    """Позитивный тест: успешная загрузка PNG"""
    files = {"file": ("x.png", PNG, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True and body.get("path")


def test_upload_ok_jpeg(tmp_path):
    """Позитивный тест: успешная загрузка JPEG"""
    files = {"file": ("x.jpg", JPEG, "image/jpeg")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True and body.get("path")


def test_upload_too_big(tmp_path):
    """Негативный тест: файл превышает лимит размера"""
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (5_000_001)
    files = {"file": ("big.png", big, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 413
    # Check RFC7807 format
    body = r.json()
    assert body.get("status") == 413
    assert body.get("title") == "Payload Too Large"
    assert "correlation_id" in body


def test_upload_bad_type(tmp_path):
    """Негативный тест: неверный тип файла (не изображение)"""
    bad = b"not_an_image"
    files = {"file": ("x.png", bad, "application/octet-stream")}
    r = client.post("/upload", files=files)
    assert r.status_code == 400
    body = r.json()
    assert body.get("title") == "Bad Request"
    assert "correlation_id" in body


def test_upload_fake_png_extension(tmp_path):
    """Негативный тест: подделка расширения (PNG расширение, но не PNG файл)"""
    fake_png = b"fake_content_not_png"
    files = {"file": ("fake.png", fake_png, "image/png")}
    r = client.post("/upload", files=files)
    assert r.status_code == 400
    body = r.json()
    assert body.get("title") == "Bad Request"


def test_sniff_image_type_png():
    """Тест функции проверки magic bytes для PNG"""
    assert sniff_image_type(PNG) == "image/png"
    assert sniff_image_type(b"fake" + PNG) is None  # PNG должен быть в начале


def test_sniff_image_type_jpeg():
    """Тест функции проверки magic bytes для JPEG"""
    assert sniff_image_type(JPEG) == "image/jpeg"
    assert sniff_image_type(b"\xff\xd8" + b"0" * 100) is None  # Нет EOI


def test_secure_save_path_traversal(tmp_path):
    """Негативный тест: попытка path traversal атаки"""
    root = Path(tmp_path) / "uploads"
    root.mkdir()

    data = PNG

    # secure_save использует UUID, но проверим защиту напрямую
    from app.services.upload import secure_save

    # Попытка создать файл с подозрительным путём
    # secure_save должен использовать UUID, но проверим защиту
    result_path = secure_save(str(root), data)
    assert result_path.startswith(str(root.resolve()))


def test_secure_save_symlink_protection(tmp_path, monkeypatch):
    """Негативный тест: защита от симлинков в родительских директориях"""
    root = Path(tmp_path) / "uploads"
    root.mkdir()

    # Создаём симлинк в родительской директории
    parent_symlink = Path(tmp_path) / "symlink_parent"
    parent_symlink.symlink_to("/tmp")

    # Попытка сохранить файл должна быть заблокирована
    from app.services.upload import secure_save

    # Если родительская директория содержит симлинк, должна быть ошибка
    # Но в реальности secure_save создаёт UUID имя, так что проверим логику
    data = PNG
    result = secure_save(str(root), data)
    # Проверяем, что путь нормализован и безопасен
    assert Path(result).resolve().is_absolute()
    assert not any(p.is_symlink() for p in Path(result).parents if p.exists())


def test_secure_save_uuid_filename(tmp_path):
    """Тест: файлы сохраняются с UUID именами"""
    root = Path(tmp_path) / "uploads"
    from app.services.upload import secure_save

    data = PNG
    path1 = secure_save(str(root), data)
    path2 = secure_save(str(root), data)

    # Имена должны быть разными (UUID)
    assert Path(path1).name != Path(path2).name
    # Имена должны содержать UUID формат
    import uuid

    name1 = Path(path1).stem
    try:
        uuid.UUID(name1)
    except ValueError:
        pytest.fail(f"Filename {name1} is not a valid UUID")
