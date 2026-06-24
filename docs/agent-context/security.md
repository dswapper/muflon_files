# Безопасность

## Секреты и конфигурация

Все секреты — в `.env` (не коммитить). Шаблон: `.env.example`.

| Переменная | Чувствительность | Назначение |
|------------|------------------|------------|
| `BOT_TOKEN` | **Критично** | Токен Telegram Bot API |
| `POSTGRES_PASSWORD` | **Критично** | Пароль БД |
| `REDIS_PASSWORD` | **Высокая** | Пароль Redis |
| `DEBUG` | Средняя | Hot-reload; в prod = `0` |
| `GHCR_IMAGE` | Низкая | Образ Docker в GHCR |

Чтение env: `environs.Env` в `bot/config.py`. При старте без `BOT_TOKEN` — только `logger.error`, бот не падает явно.

### Рекомендации по паролям

README предупреждает: **не использовать спецсимволы** в паролях Postgres/Redis (возможны проблемы с URL/compose).

### CI/CD секреты (GitHub Environment `production`)

Хранятся в GitHub Secrets / Variables:

- `BOT_TOKEN`, `POSTGRES_*`, `REDIS_*`, `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`
- Variable: `GHCR_IMAGE`

Workflow генерирует `.env` на сервере через heredoc — секреты не в репозитории.

## Авторизация в боте

- Роли: `user`, `admin` (таблица `roles`, M2M `user_roles`)
- Проверка: декоратор `@has_role('admin')` в `bot/core/decorators.py`
- При отказе: `PermissionDenied` → сообщение пользователю через error handler
- **Нет** механизма назначения admin через бота в коде — роли задаются в БД вручную (миграция seed: `user`, `admin`)

## Угрозы и поверхность атаки

| Угроза | Текущее состояние | Рекомендация |
|--------|-------------------|--------------|
| Утечка `BOT_TOKEN` | В `.env`, в GH Actions secrets | Не логировать; ротация при компрометации |
| SQL injection | SQLAlchemy ORM, параметризованные запросы | Сохранять стиль ORM |
| Broadcast abuse | Только `admin` | Аудит назначения admin-ролей |
| HTML injection в broadcast | `parse_mode='html'` из `reply_to_message.html_text` | Admin-only; риск при компрометации admin-аккаунта |
| Redis без auth в dev | Compose требует пароль | Не открывать 6379 наружу в prod |
| Postgres exposed | Порт 5432 в `docker-compose.yml` | В prod ограничить сеть/firewall |
| SSH deploy key | В secrets | Минимальные права на сервере |

## Логирование

`loguru` в `LoggingMiddleware` и error handler.

**Логируется:**

- Команды (текст начинается с `/`) — user id
- Сообщения, содержащие паттерн муфлона — **полный текст сообщения**

**Не логировать (рекомендация):**

- `BOT_TOKEN`, пароли, содержимое `.env`
- TODO: уточнить политику логирования PII (тексты сообщений пользователей)

## Error handling

`bot/handlers/exception.py`:

- `CustomException` → ответ пользователю с `message`
- Все исключения → `logger.exception` (включая stack trace)

## MCP и внешние инструменты

Конфиг: `.cursor/mcp.json`. Секреты только через `${env:...}`. См. `.cursor/mcp.example.json`.

## Docker

- Образ: `python:3.10-alpine`, non-root не настроен явно
- При старте контейнера: `alembic upgrade head` перед запуском бота

## Известные пробелы

- Нет rate limiting на команды
- Нет валидации длины входящих сообщений
- Callback-кнопки игры не защищены (обработчики отсутствуют)
- `subscribe_chat` / `unsubscribe_chat` не реализованы — поле `is_subscribed` меняется только в БД
