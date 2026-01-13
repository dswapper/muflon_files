from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.exceptions import NotFound
from bot.models import Muflon


class MuflonService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user) -> Muflon:
        muflon = Muflon(
            user=user
        )
        self.session.add(muflon)

        await self.session.flush()
        return muflon
