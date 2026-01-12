from typing import Any, Dict, Callable
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from bot.container import container
from bot.services.user_service import UserService


class ServicesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Any],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        container.register(AsyncSession, instance=data["db"])

        data["user_service"]: UserService = container.resolve(UserService)

        return await handler(event, data)
