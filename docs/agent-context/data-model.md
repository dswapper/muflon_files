# Модель данных

## ER-схема (логическая)

```
roles ←── user_roles ──→ users ──1:1──→ muflons
                              │
chats (отдельно, по telegram chat_id)

files (кэш Telegram file_id по пути на диске)
```

## Таблицы

### users

| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | Integer | PK |
| tg_id | Integer | UNIQUE, NOT NULL, INDEX |
| created_at | Timestamptz | server default now() |
| updated_at | Timestamptz | on update |

Связи: `roles` (M2M), `muflon` (1:1, cascade delete).

### roles

| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | Integer | PK |
| name | String(256) | UNIQUE, INDEX |

Seed при миграции: `user`, `admin`.

### user_roles

| Колонка | Тип | FK |
|---------|-----|-----|
| user_id | Integer | users.id CASCADE |
| role_id | Integer | roles.id |

Composite PK: `(user_id, role_id)`.

### muflons

| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | Integer | PK |
| user_id | Integer | FK users.id UNIQUE, CASCADE |
| size | Integer | default 0, server_default `0` |
| created_at, updated_at | Timestamptz | TimestampMixin |

Свойство `size_human` в модели ссылается на `size_mm`, которого **нет в модели** — вероятный баг.

### chats

| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | Integer | PK (внутренний) |
| chat_id | BigInteger | UNIQUE, INDEX (Telegram chat id) |
| type | Enum ChatType | `chat_type_enum` |
| is_active | Boolean | default True |
| is_subscribed | Boolean | default True |
| created_at, updated_at | Timestamptz | — |

`ChatType`: `private`, `group`, `supergroup`, `channel`.

### files

| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | Integer | PK |
| path | String | UNIQUE, INDEX |
| hash | String(64) | SHA-256 hex |
| file_id | String | nullable — Telegram file_id |
| created_at, updated_at | Timestamptz | — |

## Mixins

- `ReprMixin` — автогенерация `__repr__`
- `TimestampMixin` — `created_at`, `updated_at`

## Миграции Alembic

Цепочка (head = `28f595ebdc90`):

```
be4425c4ddc2 (init)
  → 36f71619514a (users, roles, user_roles + seed)
  → e9cd2688254f (muflons)
  → 24398b8baa46 (modern style)
  → ee2c44a6bf41 (timestamps)
  → 9f7c9c1476bf (chats)
  → 28f595ebdc90 (files)  ← HEAD
```

Конфиг: `alembic.ini`, `migrations/env.py` импортирует `bot.models.*` и `metadata` из `bot.db`.

Запуск: `poetry run alembic upgrade head` (в Dockerfile — перед стартом бота).

## Инварианты

1. Один `User` на `tg_id`.
2. Один `Muflon` на `User` (unique `user_id`).
3. Новый пользователь всегда получает роль `user` и пустого муфлона.
4. `Role.name` хранится в lower case при lookup (`get_role_by_name`).
5. `File.path` уникален; при изменении файла на диске hash не совпадёт → сброс `file_id`.
6. Чат регистрируется при первом сообщении через middleware.

## Не в БД (планируется, TODO.md)

- Items / Inventory
- Modifiers (баффы/дебафы)
- Activities (кулдауны)
- Валюта, PVP, магазин
- Поля: последний сон, кормление, помывка (упомянуты в TODO как частично сделанные — в текущей модели `Muflon` только `size`)

## Транзакции

- `get_session()` — `async with session.begin()`
- `UserService.create` вызывает `session.commit()` явно
- `DbSessionMiddleware` открывает сессию на весь update

TODO: уточнить согласованность commit/begin между middleware и сервисами.
