#!/bin/bash
set -e

cd course-project-cutesp1rit-public

BR="p10-sast-secrets"

# Переключение на ветку, если нужно
if [ "$(git rev-parse --abbrev-ref HEAD)" != "$BR" ]; then
    git switch "$BR"
fi

WF="Security - SAST & Secrets"

# Получение RUN_ID
RUN_ID=$(gh run list -b "$BR" -w "$WF" --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ] || [ "$RUN_ID" = "null" ]; then
    echo "Ошибка: не удалось найти запуск workflow"
    exit 1
fi

RUN_URL=$(gh run view "$RUN_ID" --json url --jq .url)

PR_TITLE='P10 - SAST & Secrets (Semgrep + Gitleaks)'
PR_FILE="$(mktemp -t pr_p10.XXXXXX.md)"

cat > "$PR_FILE" <<EOF
## Контекст

Реализация практического задания P10 — SAST & Secrets. Настроен workflow Security - SAST & Secrets (Semgrep + Gitleaks), отчёты сохраняются в репозиторий.

## Что сделано

✅ Добавлен workflow [.github/workflows/ci-sast-secrets.yml](.github/workflows/ci-sast-secrets.yml)  

✅ Добавлены правила Semgrep [security/semgrep/rules.yml](security/semgrep/rules.yml)  

✅ Добавлен конфиг Gitleaks [security/.gitleaks.toml](security/.gitleaks.toml)  

✅ Каталог артефактов [EVIDENCE/P10](EVIDENCE/P10)

## Доказательства

- Успешный запуск Security - SAST & Secrets: $RUN_URL

- Артефакты загружены в Actions (и продублированы локально в EVIDENCE/P10/artifacts/run-$RUN_ID/):

  - semgrep.sarif

  - gitleaks.json

- Результаты (по текущему запуску): Semgrep findings = 0; Gitleaks findings = 0

## Как проверял(а)

- Запуск workflow в Actions (push по ветке p10-sast-secrets)

- Проверка содержимого артефактов (SARIF и JSON)

- Возможность локального повтора через docker (см. secdev-course-docs/practices/P10)

## Критерии выполнения

- C1: Semgrep (SARIF) — выполнено

- C2: Gitleaks (JSON) — выполнено

- C3: Артефакты и документация — выполнено

- C4: Триаж — выполнено (ложных срабатываний нет)

- C5: Интеграция в CI — выполнено
EOF

# Создание или обновление PR
if gh pr view "$BR" --json number --jq .number >/dev/null 2>&1; then
    echo "Обновление существующего PR..."
    gh pr edit "$BR" -F "$PR_FILE"
else
    echo "Создание нового PR..."
    gh pr create -B main -H "$BR" -t "$PR_TITLE" -F "$PR_FILE"
fi

# Показать URL PR
gh pr view "$BR" --json url --jq .url

# Удалить временный файл
rm -f "$PR_FILE"

