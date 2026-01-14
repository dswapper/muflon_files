from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.decorators import has_role
from bot.keyboards.game import game_menu_kb
from bot.config import StaticPaths
from bot.services.file_service import FileService

router = Router()


@router.message(Command("keys"))
@has_role('admin')
async def keyboard(message: Message, bot: Bot, file_service: FileService, **kwargs):
    path = StaticPaths.cool_muflon_path

    media, file = await file_service.get_media(path)

    msg = await bot.send_photo(
        chat_id=message.chat.id,
        photo=media,
        reply_markup=game_menu_kb,
        caption="🐏 Ваш муфлон\nРазмер: 1 м\nНастроение: Отличное",
    )

    if file.file_id is None:
        await file_service.update_file_id(file, msg.photo[-1].file_id)
