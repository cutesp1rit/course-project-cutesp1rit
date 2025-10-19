# ADR-002: RFC 7807 error responses (problem+json)
Дата: 2025-10-19
Статус: Accepted

## Context
Нужен единый формат ошибок для клиентов и аудита, включая `correlation_id`.

## Decision
- Ввести helper `problem(status, title, detail, type_, extras)`.
- Для 4xx/5xx возвращать `application/problem+json` с `correlation_id`.

## Alternatives
- Оставить произвольные JSON ошибки — минусы: нет стандарта, сложнее логировать.

## Consequences
- Единый контракт ошибок, проще трассировать инциденты.

## Security impact
Меньше утечек деталей, стандартизация и маскирование.

## Rollout plan
Подключить helper к новым эндпойнтам, постепенно покрыть существующие.

## Links
- NFR: NFR-01, NFR-02
- Threat Model: F1, R2
- Tests: `tests/test_upload.py::test_upload_reject_bad_type`
