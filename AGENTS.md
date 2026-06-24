# Agent workflow — Файлы Муфлона

Telegram-бот на **aiogram 3**, **PostgreSQL**, **Redis**, деплой через **Docker** и **GitHub Actions**.

## Slash-команды (режимы)

**Без команды** — режим `default`. **Первая строка каждого ответа агента:** `mode: <имя>` (например `mode: write`).

| Команда | Назначение |
|---------|------------|
| `/default` | Чат-консультант, без правок кода (также по умолчанию) |
| `/init` | Осмотр репозитория → `docs/agent-context/` |
| `/analyze` | Проектирование → `docs/agent-tasks/` |
| `/write` | Реализация по запросу и ТЗ |
| `/review` | Ревью diff (3 обязательных раздела) |

Рекомендуемый порядок для новой фичи: **`/init`** (если контекста нет) → **`/analyze`** → **`/write`** → **`/review`**.

## Документация для агента

- **`docs/agent-context/`** — архитектура, безопасность, контракты, модели, операции (создаёт `/init`).
- **`docs/agent-tasks/`** — ТЗ и задания (создаёт `/analyze`).

## Правила

- `.cursor/rules/agent-safety.mdc` — минимальный diff, безопасность, согласование решений.
- `.cursor/rules/agent-workflow.mdc` — режимы и опора на контекст.

## MCP

Проектный конфиг: `.cursor/mcp.json`. Шаблон с примерами: `.cursor/mcp.example.json`.

1. Скопируйте нужные серверы из example в `mcp.json`.
2. Задайте переменные окружения (`GITHUB_TOKEN`, `DATABASE_URL` и т.д.) — **не** храните секреты в json.
3. Перезагрузите окно Cursor (Reload Window) и проверьте **Settings → MCP**.

Поддерживается интерполяция: `${workspaceFolder}`, `${env:NAME}`, `${userHome}`.
