import punq

from bot.services.muflon_service import MuflonService
from bot.services.user_service import UserService

container = punq.Container()

container.register(UserService, UserService)
container.register(MuflonService, MuflonService)
