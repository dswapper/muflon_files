import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from bot.core.enums.chat_type import ChatType
from bot.db import Base
from bot.models.mixins import ReprMixin, TimestampMixin


class Chat(Base, ReprMixin, TimestampMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, index=True)

    type: Mapped[ChatType] = mapped_column(
        sa.Enum(ChatType, name="chat_type_enum")
    )

    is_active: Mapped[bool] = mapped_column(default=True)
    is_subscribed: Mapped[bool] = mapped_column(default=True)
