from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.decorators import has_role
from bot.services.chat_service import ChatService
from bot.services.user_service import UserService

router = Router()


@router.message(Command("profile"))
@has_role('admin')
async def profile_handler(message: Message, user_service: UserService, **kwargs):
    user = await user_service.get_user_by_tg_id_or_create(message.from_user.id)
    await message.answer(str(user) + '\n' + str(user.roles) + '\n' + str(user.muflon))


@router.message(Command("chats"))
@has_role('admin')
async def chats_handler(message: Message, chat_service: ChatService, **kwargs):
    chats = await chat_service.get_all_active_chats()

    answer_lines = ["Список всех активных и зарегистрированных чатов:"]
    if len(chats) == 0:
        answer_lines.append("Пока в боте нет чатов")
    for chat in chats:
        answer_lines.append(f"- ID: {chat.id}, Тип: {chat.type.value}, Подписка: {chat.is_subscribed}")

    answer_text = "\n".join(answer_lines)

    await message.answer(answer_text)


@router.message(Command("broadcast"))
@has_role('admin')
async def broadcast_handler(message: Message, bot: Bot, chat_service: ChatService, **kwargs):
    chats = await chat_service.get_all_subscribed_chats()

    if not message.reply_to_message:
        await message.answer('Для работы команды нужно переслать сообщение.')
        return

    for chat in chats:
        try:
            await bot.send_message(chat_id=chat.chat_id, text=message.reply_to_message.html_text, parse_mode='html')
        except TelegramBadRequest as e:
            await message.answer(text=f'Ошибка отправки в чат №{chat.id}: {e.message}')

    await message.answer('Успешно.')
