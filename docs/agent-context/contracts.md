# Контракты

## Команды бота (Telegram)

### Публичные (без роли)

| Команда | Handler | Поведение |
|---------|---------|-----------|
| `/start` | `muflonize.start_handler` | «Привет! Я Муфлончик.» |
| `/help` | `muflonize.help_handler` | «Я не могу тебе помочь...» |
| `/muflonize` | `muflonize.muflonize_handler` | Маскирует `reply_to_message.text`; без reply — подсказка |
| `/game` | `game.keyboard` | Фото муфлона + inline-клавиатура + захардкоженный caption |

### Неявный триггер

| Условие | Handler | Поведение |
|---------|---------|-----------|
| Текст содержит `муфл...` (regex) | `muflonize.message_with_muflon_handler` | Reply с `muflonize(text)` |

Паттерн: `MUFFLON_PATTERN` / `MufflonFilter` — `r"муф(?:л(?:о(?:н)?)?)?"`, case-insensitive.

### Admin-only (`@has_role('admin')`)

| Команда | Handler | Поведение |
|---------|---------|-----------|
| `/profile` | `admin.profile_handler` | User + roles + muflon (str repr) |
| `/chats` | `admin.chats_handler` | Список активных чатов (`is_active=True`) |
| `/broadcast` | `admin.broadcast_handler` | Рассылка `reply_to_message` в подписанные чаты (`is_subscribed=True`), HTML |
| `/keys` | `keyboard_callbacks_test.keyboard` | Тест inline-клавиатуры (admin) |

## Inline keyboard (callback_data)

Клавиатура: `bot/keyboards/game.py` → `game_menu_kb`

| callback_data | Кнопка | Обработчик |
|---------------|--------|------------|
| `muflon_feed` | Покормить | **Нет** |
| `muflon_wash` | Помыть | **Нет** |
| `muflon_sleep` | Уложить спать | **Нет** |
| `muflon_pvp-start` | Бой / Магазин | **Нет** |
| `muflon_mini-games` | Мини-игры / Инвентарь | **Нет** |

## Сервисы (внутренний API)

### UserService

| Метод | Вход | Выход / ошибки |
|-------|------|----------------|
| `get_user_by_id` | `user_id` | `User` или `NotFound` |
| `get_user_by_tg_id` | `tg_id` | `User` или `NotFound` |
| `get_user_by_tg_id_or_create` | `tg_id` | `User` (создаёт с ролью `user` + Muflon) |
| `create` | `tg_id` | `User` + commit |
| `get_role_by_name` | `name` | `Role` или `NotFound` |
| `add_role` / `remove_role` | `User`, `role_name` | — |

### MuflonService

| Метод | Вход | Выход |
|-------|------|-------|
| `create` | `user` | `Muflon` (size=0) |

### ChatService

| Метод | Вход | Выход |
|-------|------|-------|
| `get_chat_by_chat_id` | `chat_id` | `Chat \| None` |
| `get_all_active_chats` | — | `Sequence[Chat]` |
| `get_all_subscribed_chats` | — | active + subscribed |
| `create` | `chat_id`, `ChatType` | `Chat` |
| `create_if_not_exist` | `chat_id`, `ChatType` | `Chat` |

### FileService

| Метод | Вход | Выход |
|-------|------|-------|
| `get_file_by_path` | `path` | `File \| None` |
| `create` | `path`, `file_id?` | `File` (hash SHA-256) |
| `get_file_by_path_or_create` | `path`, `file_id?` | `File` (пересчёт hash при изменении файла) |
| `update_file_id` | `File`, `new_file_id` | `File` |
| `get_media` | `PosixPath` | `(FSInputFile \| file_id str, File)` |

### muflonize (pure function)

```python
muflonize(text: str) -> str
```

Заменяет каждую букву на `█`, кроме совпадений с паттерном «муфлон». Небуквенные символы сохраняются.

## Исключения (контракт для handlers)

| Класс | Сообщение по умолчанию |
|-------|------------------------|
| `CustomException` | «Упс... Что-то пошло не так...» |
| `InvalidUsage` | кастомное |
| `NotFound` | «Не найдено.» |
| `PermissionDenied` | «У вас нет доступа к данной команде.» |

## Внешние API

### Telegram Bot API

- Transport: long polling (`dp.start_polling`)
- Отправка: `Message.answer`, `Bot.send_message`, `Bot.send_photo`
- Broadcast: HTML parse mode из пересланного сообщения

### PostgreSQL

- Driver: `asyncpg` via `postgresql+asyncpg://`
- URI из `bot/config.py:SQLALCHEMY_DATABASE_URI`

### Redis

- Client: `redis.asyncio.Redis`
- Использование: `RedisStorage` для FSM aiogram
- Auth: `REDIS_PASSWORD`

### GHCR (деплой)

- Образ: `${GHCR_IMAGE}:latest` и `:${sha}`
- Registry: `ghcr.io`

## Статические ресурсы

| Путь | Использование |
|------|---------------|
| `bot/static/images/muflon_cool.png` | `StaticPaths.cool_muflon_path` — фото в `/game`, `/keys` |
