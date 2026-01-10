from aiogram import BaseMiddleware


class ServicesMiddleware(BaseMiddleware):
    def __init__(self, services: dict):
        super().__init__()
        self.services = services

    async def __call__(self, handler, event, data):
        data.update(self.services)
        return await handler(event, data)
