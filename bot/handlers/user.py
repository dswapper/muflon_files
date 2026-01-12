from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.decorators import has_role
from bot.services.user_service import UserService

router = Router()


@router.message(Command("profile"))
@has_role('admin')
async def profile_handler(message: Message, user_service: UserService, **kwargs):
    user = await user_service.get_user_by_tg_id_or_create(message.from_user.id)
    await message.answer(str(user) + '\n' + str(user.roles))
