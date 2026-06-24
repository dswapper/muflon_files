# Архитектура

## Обзор

Монолитный async Telegram-бот. Точка входа: `python -m bot` → `bot/__main__.py`.

```
Telegram API
     │
     ▼
┌─────────────────────────────────────────┐
│  aiogram Dispatcher (long polling)      │
│  FSM storage: Redis (RedisStorage)      │
└─────────────────────────────────────────┘
     │
     ▼ outer middleware (на каждый update)
┌──────────────────┐  ┌──────────────────┐
│ DbSessionMiddleware │ ServicesMiddleware │
│  → data["db"]       │  → *\_service      │
└──────────────────┘  └──────────────────┘
     │
     ▼ message middleware
┌──────────────────┐  ┌──────────────────┐
│ LoggingMiddleware │  │ SaveChatMiddleware │
└──────────────────┘  └──────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Routers (handlers)                     │
│  admin │ exception │ muflonize │ game   │
│  keyboard_callbacks_test                │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Services (бизнес-логика)               │
│  User │ Muflon │ Chat │ File            │
└─────────────────────────────────────────┘
     │
     ▼
┌──────────────────┐  ┌──────────────────┐
│  PostgreSQL       │  │  Redis            │
│  (SQLAlchemy)     │  │  (FSM + пароль)   │
└──────────────────┘  └──────────────────┘
```

## Слои

| Слой | Путь | Ответственность |
|------|------|-----------------|
| Entry | `bot/__main__.py` | Bootstrap: Bot, Dispatcher, Redis, роутеры, middleware |
| Config | `bot/config.py` | Env-переменные, `MUFFLON_PATTERN`, `StaticPaths` |
| Handlers | `bot/handlers/` | Команды и обработчики Telegram-событий |
| Filters | `bot/filters/` | Условия маршрутизации (`MufflonFilter`) |
| Keyboards | `bot/keyboards/` | Inline-клавиатуры |
| Services | `bot/services/` | Бизнес-логика, работа с БД |
| Models | `bot/models/` | SQLAlchemy ORM |
| DB | `bot/db.py` | Engine, sessionmaker, `Base` |
| Core | `bot/core/` | Декораторы (`has_role`), исключения, enums |
| Middlewares | `bot/middlewares/` | Сессия БД, DI сервисов, логи, сохранение чатов |
| Migrations | `migrations/` | Alembic |

## Dependency Injection

`punq.Container` в `bot/container.py`:

- Регистрирует: `UserService`, `MuflonService`, `ChatService`, `FileService`
- `ServicesMiddleware` на каждый update создаёт контейнер и регистрирует `AsyncSession` из `data["db"]`
- Сервисы попадают в handlers через kwargs: `user_service`, `chat_service`, `file_service`, `muflon_service`

Зависимости сервисов:

- `UserService` → `AsyncSession`, `MuflonService`
- `MuflonService`, `ChatService`, `FileService` → `AsyncSession`

## Middleware (порядок регистрации)

```python
# bot/__main__.py
dp.message.middleware(LoggingMiddleware())
dp.message.middleware(SaveChatMiddleware())
dp.update.outer_middleware(DbSessionMiddleware(get_session))
dp.update.outer_middleware(ServicesMiddleware())
```

| Middleware | Scope | Назначение |
|------------|-------|------------|
| `DbSessionMiddleware` | update (outer) | Открывает `AsyncSession` → `data["db"]` |
| `ServicesMiddleware` | update (outer) | Резолвит сервисы в `data` |
| `LoggingMiddleware` | message | Логирует команды и сообщения с «муфлон» |
| `SaveChatMiddleware` | message | `ChatService.create_if_not_exist` при каждом сообщении |

**Замечание:** `DbSessionMiddleware` принимает `get_session` (async contextmanager), хотя type hint указывает `sessionmaker`. Транзакция: `get_session` оборачивает сессию в `session.begin()`.

## Роутеры (порядок подключения)

1. `admin` — команды с ролью `admin`
2. `exception` — глобальный error handler
3. `muflonize` — основная функциональность маскировки
4. `keyboard_callbacks_test` — тест клавиатуры (`/keys`, admin)
5. `game` — прототип игры (`/game`)

## Ключевые потоки

### Муфлонизация текста

1. Сообщение с текстом, содержащим паттерн `муфл...` → `MufflonFilter`
2. `bot/services/muflonize.py:muflonize()` — замена букв на `█`, кроме разрешённого паттерна
3. Ответ reply с замаскированным текстом

Команда `/muflonize` — то же для `reply_to_message.text`.

### Создание пользователя

1. `@has_role` или явный вызов → `UserService.get_user_by_tg_id_or_create`
2. Создаёт `User`, назначает роль `user`, создаёт связанный `Muflon`

### Сохранение чата

1. Любое message-событие → `SaveChatMiddleware`
2. `ChatService.create_if_not_exist(chat_id, ChatType)`

### Файлы Telegram (кэш file_id)

1. `FileService.get_media(path)` — SHA-256 хеш файла на диске
2. Если `file_id` в БД есть — отправка по `file_id`, иначе `FSInputFile`
3. После отправки — `update_file_id` для кэширования

## Режим разработки

`DEBUG=1` → `watchgod.run_process` перезапускает бота при изменениях.

## Внешние зависимости (runtime)

| Компонент | Назначение |
|-----------|------------|
| Telegram Bot API | Polling, отправка сообщений/фото |
| PostgreSQL | Персистентные данные |
| Redis | FSM storage aiogram (`RedisStorage`) |
