from aiogram import Router, F
from aiogram.types import ErrorEvent, Message

from bot.core.exceptions import CustomException

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_custom_exception(event: ErrorEvent, message: Message):
    if isinstance(event.exception, CustomException):
        text = str(event.exception.message)
    else:
        text = CustomException.default_message

    await message.answer(text)