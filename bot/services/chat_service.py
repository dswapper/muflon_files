from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.enums.chat_type import ChatType
from bot.models import Chat


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_chat_by_chat_id(self, chat_id: int) -> Chat:
        chat = (await self.session.execute(select(Chat).where(Chat.chat_id == chat_id))).scalar_one_or_none()
        return chat

    async def get_all_active_chats(self) -> Sequence[Chat]:
        chat = (await self.session.execute(select(Chat).where(Chat.is_active == True))).scalars().all()
        return chat

    async def get_all_subscribed_chats(self) -> Sequence[Chat]:
        chat = ((await
                self.session.execute(select(Chat).where(Chat.is_active == True, Chat.is_subscribed == True)))
                .scalars().all())
        return chat

    async def create(self, chat_id: int, type: ChatType) -> Chat:
        chat = Chat(
            chat_id=chat_id,
            type=type
        )
        self.session.add(chat)

        await self.session.flush()
        return chat

    async def create_if_not_exist(self, chat_id: int, type: ChatType) -> Chat:
        chat = await self.get_chat_by_chat_id(chat_id)
        if chat is None:
            chat = await self.create(chat_id=chat_id, type=type)
        return chat

