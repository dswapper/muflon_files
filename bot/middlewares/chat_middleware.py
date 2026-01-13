from aiogram import BaseMiddleware

from bot.core.enums.chat_type import ChatType
from bot.services.chat_service import ChatService


class SaveChatMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        chat = event.chat
        chat_service: ChatService = data['chat_service']
        if chat:
            type = ChatType(chat.type) if chat.type in ChatType._value2member_map_ else ChatType.PRIVATE
            await chat_service.create_if_not_exist(
                chat_id=chat.id,
                type=type
            )
        return await handler(event, data)
