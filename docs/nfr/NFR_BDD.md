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
