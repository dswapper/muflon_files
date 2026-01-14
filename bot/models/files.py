import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from bot.db import Base
from bot.models.mixins import TimestampMixin, ReprMixin


class File(Base, ReprMixin, TimestampMixin):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)

    path: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hash: Mapped[str] = mapped_column(sa.String(64), nullable=False)

    file_id: Mapped[str | None] = mapped_column(nullable=True)
