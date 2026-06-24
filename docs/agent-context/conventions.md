# Соглашения и паттерны

## Структура каталогов

```
bot/
  __main__.py          # entry point
  config.py            # env, константы
  db.py                # SQLAlchemy engine/session
  container.py         # punq DI
  handlers/            # aiogram routers
  services/            # бизнес-логика
  models/              # ORM
  middlewares/
  filters/
  keyboards/
  core/                # decorators, exceptions, enums
  static/images/       # статика для бота
migrations/            # Alembic
docs/
  agent-context/       # контекст для AI-агентов
  source/              # Sphinx
```

## Стиль кода

- Python 3.10 (ограничение в `pyproject.toml`: `<3.11`)
- Async/await везде в handlers и services
- SQLAlchemy 2.0 style: `Mapped`, `mapped_column`, `select()`
- Type hints на моделях и сигнатурах сервисов
- Логирование: `loguru`

## Паттерны

### Handler

```python
router = Router()

@router.message(Command("example"))
@has_role('admin')  # опционально
async def handler(message: Message, user_service: UserService, **kwargs):
    ...
```

Сервисы инжектятся через `ServicesMiddleware` по имени параметра.

### Service

- Класс с `__init__(self, session: AsyncSession, ...)`
- Запросы через `await self.session.execute(select(...))`
- Ошибки домена → `NotFound`, `PermissionDenied` из `bot.core.exceptions`

### Middleware

- Наследование от `BaseMiddleware` (aiogram) или callable-класс (`DbSessionMiddleware`)
- Мутация `data: Dict[str, Any]` для передачи зависимостей

### Модель

```python
class Entity(Base, ReprMixin, TimestampMixin):
    __tablename__ = "entities"
    id: Mapped[int] = mapped_column(primary_key=True)
```

Экспорт моделей: `bot/models/__init__.py`.

## Как добавить новую команду

1. Создать/расширить router в `bot/handlers/`
2. Подключить router в `bot/__main__.py` → `dp.include_router(...)`
3. Бизнес-логику — в `bot/services/`
4. При необходимости — модель + миграция Alembic
5. Зарегистрировать сервис в `bot/container.py` и `ServicesMiddleware`
6. Обновить `docs/agent-context/contracts.md` (через `/init`)

## Как добавить роль / проверку доступа

1. Добавить запись в `roles` (миграция или SQL)
2. Использовать `@has_role('name')` или `@has_any_role(...)`
3. Назначение роли пользователю: `UserService.add_role` (нет публичной команды)

## Как добавить callback-кнопку

1. Кнопка в `bot/keyboards/`
2. Router с `@router.callback_query(F.data == "...")`
3. Подключить router в `__main__.py`

Сейчас callback'и игры **не подключены** — образец клавиатуры есть.

## Миграции

1. Изменить модели в `bot/models/`
2. `poetry run alembic revision --autogenerate -m "описание"`
3. Проверить сгенерированный файл в `migrations/versions/`
4. `alembic upgrade head`

## Тестирование

Dev-зависимости: `pytest`, `pytest-asyncio`. Тестов в репозитории практически нет — см. `TODO.md`.

## Agent workflow (Cursor)

| Режим | Когда |
|-------|-------|
| `/init` | Первичный осмотр / обновление `docs/agent-context/` |
| `/analyze` | Проектирование → `docs/agent-tasks/` |
| `/write` | Реализация |
| `/review` | Ревью перед merge |

Правила: `.cursor/rules/agent-safety.mdc`, `agent-workflow.mdc`.

## Что не делать

- Не коммитить `.env`
- Не расширять scope рефакторингом без запроса
- Не менять схему БД без миграции
- Не хардкодить секреты
