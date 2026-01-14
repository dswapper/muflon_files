from aiogram import Router, F
from aiogram.types import ErrorEvent, Message
from loguru import logger

from bot.core.exceptions import CustomException

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_custom_exception(event: ErrorEvent, message: Message):
    if isinstance(event.exception, CustomException):
        await message.answer(str(event.exception.message))

    logger.exception(event.exception)
    return True
