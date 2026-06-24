# Agent context — Файлы Муфлона

База знаний проекта для Cursor-агентов. Обновляется командой `/init`.

| Поле | Значение |
|------|----------|
| **Дата обновления** | 2026-06-24 |
| **Коммит** | `f4daf49` — WIP: игра муфлон |
| **Версия (Poetry)** | 0.1.0 |
| **Python** | 3.10 |
| **Стек** | aiogram 3, SQLAlchemy 2 (async), PostgreSQL 16, Redis 7, Alembic, punq (DI) |

## О проекте

**Файлы Муфлона** — Telegram-бот, маскирующий текст символами `█`, кроме слова «муфлон» и его производных. Дополнительно: роли пользователей, учёт чатов, рассылка, зачатки игры-тамагочи с муфлоном.

## Оглавление

| Документ | Содержание |
|----------|------------|
| [architecture.md](./architecture.md) | Слои, middleware, DI, потоки данных |
| [security.md](./security.md) | Секреты, угрозы, логирование |
| [contracts.md](./contracts.md) | Команды бота, сервисы, внешние API |
| [data-model.md](./data-model.md) | ORM-модели, миграции, инварианты |
| [operations.md](./operations.md) | Docker, env, CI/CD, деплой |
| [conventions.md](./conventions.md) | Стиль, структура, как добавлять фичи |

## Статус и пробелы

- Игра `/game` — UI-прототип с захардкоженными параметрами; callback-кнопки не обработаны.
- `Muflon.size_human` ссылается на несуществующее свойство `size_mm` — **TODO: уточнить/исправить**.
- `subscribe_chat` / `unsubscribe_chat` из TODO.md в коде не найдены.
- Тесты и админ-панель — не реализованы (см. `TODO.md`).

## Связанные артефакты

- `AGENTS.md` — workflow slash-команд
- `docs/agent-tasks/` — ТЗ от `/analyze`
- `TODO.md` — дорожная карта разработчика
- `docs/source/` — Sphinx-документация (отдельно от agent-context)
