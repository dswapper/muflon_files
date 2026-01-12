import punq
from bot.services.user_service import UserService

container = punq.Container()

container.register(UserService, UserService)
