import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column

from bot.db import Base
from bot.models.mixins import ReprMixin, TimestampMixin


class Muflon(Base, ReprMixin, TimestampMixin):
    __tablename__ = "muflons"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey(
            "users.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="muflon",
        lazy="selectin",
    )

    size: Mapped[int] = mapped_column(
        default=0,
        server_default="0",
        nullable=False,
    )

