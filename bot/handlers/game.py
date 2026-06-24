import textwrap

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.decorators import has_role
from bot.keyboards.game import game_menu_kb
from bot.config import StaticPaths
from bot.services.file_service import FileService

router = Router()


@router.message(Command("game"))
async def keyboard(message: Message, bot: Bot, file_service: FileService, **kwargs):
    path = StaticPaths.cool_muflon_path

    media, file = await file_service.get_media(path)

    chat = message.chat

    caption_text = textwrap.dedent(f"""
        👤 Игрок: *{chat.full_name}*
        
        🐏 Ваш Муфлон:
        
        📏 Размер: 1.2 км
        
        😊 Настроение: Ужасное
        - Сытость: 20%
        - Усталость: 15%
        - Загрязнённость: 99% ❗️ 
        - Здоровье: 60% (Восстановится через 2 часа 21 минуту)
        
        🎂 Возраст: 12 дней
        
        На размер влияет то насколько много и насколько сытно он кушает, а также его настроения.
        Настроение муфлона зависит от его усталости и загрязнённости
    """)

    msg = await bot.send_photo(
        chat_id=message.chat.id,
        photo=media,
        reply_markup=game_menu_kb,
        caption=caption_text,
        parse_mode='markdown'
    )

    if file.file_id is None:
        await file_service.update_file_id(file, msg.photo[-1].file_id)