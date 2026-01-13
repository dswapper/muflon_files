from enum import Enum


class ChatType(Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"
