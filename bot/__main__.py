import asyncio

from redis.asyncio import Redis
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config import BOT_TOKEN, DEBUG, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from bot.handlers import muflonize
from bot.middlewares.logging_middleware import LoggingMiddleware
from watchgod import run_process


async def main():
    redis = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=0,
    )

    storage = RedisStorage(redis)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    dp.message.middleware(LoggingMiddleware())

    dp.include_router(muflonize.router)

    try:
        logger.info("Bot is starting...")
        await dp.start_polling(bot)
    finally:
        logger.info("Bot is stopped!")
        await bot.session.close()
        await storage.close()


def start_bot():
    return asyncio.run(main())


if __name__ == "__main__":
    if DEBUG:
        run_process("bot", start_bot)
    else:
        start_bot()
