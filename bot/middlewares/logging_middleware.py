from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from loguru import logger

from bot.config import MUFFLON_PATTERN


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        try:
            if isinstance(event, Message) and event.text:
                user = getattr(event.from_user, "id", "unknown")

                if event.text.startswith("/"):
                    logger.info(f"Команда от {user}: {event.text}")

                elif MUFFLON_PATTERN.search(event.text):
                    logger.info(f"Сообщение от {user}: {event.text}")

            return await handler(event, data)

        except Exception as e:
            logger.exception(f"Ошибка при обработке сообщения: {e}")
            raise
