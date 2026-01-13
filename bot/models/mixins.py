import sqlalchemy as sa

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


class ReprMixin:
    """Mixin для автоматического __repr__ всех ORM-моделей."""

    def __repr__(self):
        columns = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        col_str = ", ".join(f"{k}={v!r}" for k, v in columns.items())
        return f"<{self.__class__.__name__} {{{col_str}}}>"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
