# ADR-003: Client policies (timeouts, retries, limits)
Дата: 2025-10-19
Статус: Accepted

## Context
Исходящие HTTP-запросы могут зависать или перегружать систему при ошибках.

## Decision
- Ввести разумные таймауты, ограничение ретраев (exponential backoff), лимиты размеров.

## Alternatives
- Без политик — быстрее старт, но выше риск зависаний и шторма.

## Consequences
- Больше конфигурации и тестов, но стабильнее поведение.

## Security impact
Снижается риск DoS через зависания и повторные попытки.

## Rollout plan
Добавлять политики при появлении исходящих интеграций.

## Links
- NFR: NFR-03, NFR-06
- Threat Model: F1, R6
- Tests: план на e2e/load
