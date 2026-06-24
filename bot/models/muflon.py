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

    @property
    def size_human(self) -> str:
        mm = self.size_mm

        if mm < 10:
            return f"{mm} мм"
        elif mm < 1_000:
            return f"{mm / 10:.1f} см"
        elif mm < 1_000_000:
            return f"{mm / 1_000:.2f} м"
        else:
            return f"{mm / 1_000_000:.2f} км"

