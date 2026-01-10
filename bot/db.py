from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from bot.config import SQLALCHEMY_DATABASE_URI

from contextlib import asynccontextmanager

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
metadata = Base.metadata


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e
