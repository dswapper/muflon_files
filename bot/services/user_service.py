from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.exceptions import NotFound
from bot.models import User, Role


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        user = (await self.session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if user is None:
            raise NotFound(f'Пользователь с id {user_id} не найден')
        return user

    async def get_user_by_tg_id(self, tg_id: int) -> User:
        user = (await self.session.execute(select(User).where(User.tg_id == tg_id))).scalar_one_or_none()
        if user is None:
            raise NotFound(f'Пользователь с telegram_id {tg_id} не найден')
        return user

    async def get_user_by_tg_id_or_create(self, tg_id: int) -> User:
        user = (await self.session.execute(select(User).where(User.tg_id == tg_id))).scalar_one_or_none()
        if user is None:
            user = await self.create(tg_id)
        return user

    async def create(self, tg_id: int) -> User:
        user = User(tg_id=tg_id)
        self.session.add(user)

        role = await self.get_role_by_name("user")
        user.roles.append(role)

        await self.session.commit()
        return user

    async def get_role_by_name(self, name: str) -> Role:
        role = (await self.session.execute(select(Role).where(Role.name == name.lower()))).scalar_one_or_none()
        if role is None:
            raise NotFound(f'Роль {name} не найдена!')
        return role

    async def add_role(self, user: User, role_name: str) -> None:
        role = await self.get_role_by_name(role_name)
        user.add_role(role)

    async def remove_role(self, user: User, role_name: str) -> None:
        role = await self.get_role_by_name(role_name)
        user.remove_role(role)
