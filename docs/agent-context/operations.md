# Операции

## Переменные окружения

Шаблон: `.env.example`

| Переменная | Обязательна | Default (в коде) | Описание |
|------------|-------------|------------------|----------|
| `BOT_TOKEN` | Да | — | Telegram bot token |
| `DEBUG` | Нет | `False` | `1/true/yes` → watchgod hot-reload |
| `POSTGRES_DB` | Нет | `muflon_bot_db` | Имя БД |
| `POSTGRES_USER` | Нет | `postgres` | Пользователь БД |
| `POSTGRES_PASSWORD` | Нет | `postgres` | Пароль БД |
| `POSTGRES_HOST` | Нет | `postgres` | Хост (имя сервиса в compose) |
| `POSTGRES_PORT` | Нет | `5432` | Порт |
| `REDIS_HOST` | Нет | `redis` | Хост Redis |
| `REDIS_PORT` | Нет | `6379` | Порт |
| `REDIS_PASSWORD` | Нет | `redis` | Пароль Redis |
| `GHCR_IMAGE` | Для prod | — | Образ в GHCR, напр. `ghcr.io/dswapper/muflon_files` |

## Docker Compose

### Базовый (`docker-compose.yml`)

Сервисы:

- **postgres** — `postgres:16-alpine`, порт 5432, volume `postgres_data`, healthcheck
- **redis** — `redis:7-alpine`, порт 6379, `--requirepass`, volume `redis_data`, healthcheck

Сеть: `internal` (bridge).

### Production overlay (`docker-compose.prod.yml`)

Сервис **bot**:

- Образ: `${GHCR_IMAGE}:latest` (build: none)
- `env_file: .env`
- `depends_on` postgres + redis (healthy)
- `restart: unless-stopped`

**Замечание:** в prod-файле объявлена external-сеть `muflon_bot_internal`, но bot использует сеть `internal` из базового compose. TODO: уточнить актуальную сетевую конфигурацию на сервере.

### Локальный запуск (из README)

```bash
docker compose -f docker-compose.prod.yml -f docker-compose.yml up -d
```

Только инфраструктура (без бота):

```bash
docker compose -f docker-compose.yml up -d
```

## Dockerfile

Multi-stage:

1. `python-base` — Python 3.10 alpine
2. `poetry-base` — Poetry 1.8.4 в venv
3. `muflon_tg_bot` — `poetry install --without dev`, копия кода

**CMD:**

```sh
poetry run alembic upgrade head && poetry run python -m bot
```

## Локальная разработка (без Docker)

```bash
poetry install
cp .env.example .env   # заполнить значения
# postgres + redis должны быть доступны
poetry run alembic upgrade head
DEBUG=1 poetry run python -m bot
```

Скрипт WSL: `scripts/wsl-setup.sh` (TODO: уточнить содержимое при необходимости).

## CI/CD

Workflow: `.github/workflows/deploy.yml` — **Build & Deploy**

**Триггеры:**

- Push тега `v*.*.*`
- `workflow_dispatch` (ручной)

**Шаги:**

1. Checkout
2. Login GHCR (`GITHUB_TOKEN`)
3. `docker build` + push `:latest` и `:${github.sha}`
4. rsync проекта на сервер (`/home/$SSH_USER/muflon_bot`)
5. SSH: создать `.env` из secrets, `docker compose pull`, `docker compose up -d`

**GitHub Environment:** `production`

**Secrets:** BOT_TOKEN, POSTGRES_*, REDIS_*, SSH_*

**Variables:** GHCR_IMAGE

## Деплой на сервер (требования)

- Docker + compose plugin
- Пользователь `deploy` в группе `docker`
- SSH-ключ для GitHub Actions
- См. README для полной инструкции fork/deploy

## Мониторинг и логи

- Логи бота: stdout через loguru
- Healthcheck: postgres (`pg_isready`), redis (`redis-cli ping`)
- TODO: централизованный мониторинг не настроен

## Sphinx-документация

Отдельно от agent-context:

```bash
cd docs && make html
```

Исходники: `docs/source/`, конфиг `docs/source/conf.py`.

## Полезные команды

| Действие | Команда |
|----------|---------|
| Миграции | `poetry run alembic upgrade head` |
| Новая миграция | `poetry run alembic revision --autogenerate -m "..."` |
| Запуск бота | `poetry run python -m bot` |
| Тесты | `poetry run pytest` (тестов мало/нет) |
