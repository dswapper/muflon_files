from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.user_service import UserService

router = Router()


@router.message(Command("profile"))
async def start_handler(message: Message, user_service: UserService):
    user = await user_service.get_user_by_tg_id_or_create(message.from_user.id)
    await message.answer(str(user))
