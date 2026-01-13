from typing import Any, Dict, Callable
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class DbSessionMiddleware:
    def __init__(self, session_factory: sessionmaker[AsyncSession]) -> None:
        self.session_factory: sessionmaker[AsyncSession] = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_factory() as session:
            data["db"]: AsyncSession = session
            return await handler(event, data)
