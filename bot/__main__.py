import asyncio

from redis.asyncio import Redis
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config import BOT_TOKEN, DEBUG, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from bot.db import get_session
from bot.handlers import muflonize, admin, exception, keyboard_callbacks_test, game
from watchgod import run_process

from bot.middlewares.chat_middleware import SaveChatMiddleware
from bot.middlewares.db_session_middleware import DbSessionMiddleware
from bot.middlewares.logging_middleware import LoggingMiddleware
from bot.middlewares.service_middleware import ServicesMiddleware


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
    dp.message.middleware(SaveChatMiddleware())
    dp.update.outer_middleware(DbSessionMiddleware(get_session))
    dp.update.outer_middleware(ServicesMiddleware())

    dp.include_router(admin.router)
    dp.include_router(exception.router)
    dp.include_router(muflonize.router)
    dp.include_router(keyboard_callbacks_test.router)
    dp.include_router(game.router)

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
