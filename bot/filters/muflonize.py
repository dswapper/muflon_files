from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.config import MUFFLON_PATTERN


class MufflonFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text and MUFFLON_PATTERN.search(message.text))
