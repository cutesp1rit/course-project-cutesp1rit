# NFR_BDD — Приёмка в формате Gherkin

Feature: Контракт ошибок и безопасные заголовки
  Scenario: Все ответы содержат безопасные заголовки
    Given запущено API сервиса
    When выполняется запрос к любому эндпойнту
    Then ответы содержат X-Content-Type-Options=nosniff, X-Frame-Options=DENY, Referrer-Policy=no-referrer, X-XSS-Protection=0

  Scenario: Валидационные ошибки нормализованы
    Given запущено API сервиса
    When отправляется невалидный запрос
    Then ответ имеет код 422 и тело {"error": {"code": "validation_error", "message": "invalid_request"}}

Feature: Ограничение размера тела запроса
  Scenario: Блокировка слишком больших тел
    Given развернут сервис с лимитом 1 MB на тело
    When отправляется POST с телом > 1 MB
    Then ответ имеет код 413 и тело ошибки в едином формате

Feature: Производительность GET /decks
  Scenario: p95 не превышает порог на stage
    Given нагрузка 20 RPS на протяжении 5 минут
    When собирается latency распределение
    Then p95 времени ответа ≤ 150 ms
