from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import MUFFLON_PATTERN
from bot.services.muflonize import muflonize

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я Муфлончик.")


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Я не могу тебе помочь...")


@router.message(Command("muflonize"))
async def muflonize_handler(message: Message):
    if message.reply_to_message:
        await message.answer(muflonize(message.reply_to_message.text))
    else:
        await message.answer("Для работы этой команды надо переслать сообщение.")


@router.message()
async def message_handler(message: Message):
    if MUFFLON_PATTERN.search(message.text):
        response = muflonize(message.text)
        await message.reply(response)
