from sqlalchemy import select

from bot.core.exceptions import NotFound
from bot.db import get_session
from bot.models import User, Role


class UserService:
    def __init__(self):
        pass

    @staticmethod
    async def get_user_by_id(user_id) -> User:
        async with get_session() as session:
            user = (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
            if user is None:
                raise NotFound(f'Пользователь с id {user_id} не найден')
            return user

    @staticmethod
    async def get_user_by_tg_id(tg_id) -> User:
        async with get_session() as session:
            user = (await session.execute(select(User).where(User.tg_id == tg_id))).scalar_one_or_none()
            if user is None:
                raise NotFound(f'Пользователь с telegram_id {tg_id} не найден')
            return user

    async def get_user_by_tg_id_or_create(self, tg_id) -> User:
        async with get_session() as session:
            user = (await session.execute(select(User).where(User.tg_id == tg_id))).scalar_one_or_none()
            if user is None:
                user = await self.create(tg_id)
            return user

    @staticmethod
    async def create(tg_id: int) -> User:
        async with get_session() as session:
            user = User(
                tg_id=tg_id
            )
            session.add(user)
            return user

    @staticmethod
    async def get_role_by_name(name: str) -> Role:
        async with get_session() as session:
            role = (await session.execute(select(Role).where(Role.name == name.lower()))).scalar_one_or_none()
            if role is None:
                raise NotFound(f'Роль {name} не найдена!')
            return role

    async def add_role(self, user: User, role_name: str) -> None:
        role = await self.get_role_by_name(role_name)
        user.add_role(role)

    async def remove_role(self, user: User, role_name: str) -> None:
        role = await self.get_role_by_name(role_name)
        user.remove_role(role)
