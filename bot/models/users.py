from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column

from bot.db import Base
from bot.models.mixins import ReprMixin, TimestampMixin

user_roles = sa.Table(
    "user_roles",
    Base.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id",
                                                   ondelete="CASCADE",
                                                   onupdate="CASCADE",
                                                   ), primary_key=True, nullable=False),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), primary_key=True, nullable=False),
)


class User(Base, ReprMixin, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users",
        cascade="all, delete",
        lazy="selectin",
    )

    muflon: Mapped[Optional["Muflon"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        uselist=False,
        lazy="selectin",
    )

    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)

    def has_any_role(self, role_names: tuple[str]) -> bool:
        return any(role.name in role_names for role in self.roles)

    def add_role(self, role: "Role") -> None:
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: "Role") -> None:
        if role in self.roles:
            self.roles.remove(role)


class Role(Base, ReprMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(256), unique=True, index=True)

    users: Mapped[List["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
    )

