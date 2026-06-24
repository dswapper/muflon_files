import punq

from bot.services.chat_service import ChatService
from bot.services.file_service import FileService
from bot.services.muflon_service import MuflonService
from bot.services.user_service import UserService


def create_container() -> punq.Container:
    container = punq.Container()

    container.register(UserService, UserService)
    container.register(MuflonService, MuflonService)
    container.register(ChatService, ChatService)
    container.register(FileService, FileService)

    return container
