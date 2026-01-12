from functools import wraps
from typing import Callable, Awaitable, Any, Union

from aiogram.types import Message, CallbackQuery
from bot.core.exceptions import PermissionDenied
from bot.services.user_service import UserService


def has_role(required_role: str):
    def decorator(handler: Callable[..., Awaitable[Any]]):
        @wraps(handler)
        async def wrapper(update: Union[Message, CallbackQuery], *args, **kwargs):
            user_service: UserService = kwargs.get("user_service")
            tg_id = update.from_user.id

            user = await user_service.get_user_by_tg_id_or_create(tg_id)
            if not user.has_role(required_role):
                raise PermissionDenied

            return await handler(update, *args, **kwargs)
        return wrapper
    return decorator

