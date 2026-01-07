import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN, DEBUG
from bot.handlers import muflonize
from bot.middlewares.logging_middleware import LoggingMiddleware
from watchgod import run_process


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(LoggingMiddleware())

    dp.include_router(muflonize.router)

    try:
        logger.info("Bot is starting...")
        await dp.start_polling(bot)
    finally:
        logger.info("Bot is stopped!")
        await bot.session.close()


def start_bot():
    return asyncio.run(main())


if __name__ == "__main__":
    if DEBUG:
        run_process("bot", start_bot)
    else:
        start_bot()
