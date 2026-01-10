class CustomException(Exception):
    default_message = "Упс... Что-то пошло не так. Повторите попытку позже."

    def __init__(self, message: str = default_message):
        self.message = message


class InvalidUsage(CustomException):
    def __init__(self, message: str):
        self.message = message


class NotFound(CustomException):
    def __init__(self, message: str = "Не найдено."):
        self.message = message


class PermissionDenied(CustomException):
    def __init__(self, message: str = "У вас нет доступа к данной команде."):
        self.message = message