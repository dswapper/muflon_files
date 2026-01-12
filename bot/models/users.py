import sqlalchemy as sa
from sqlalchemy.orm import relationship

from bot.db import Base
from bot.models.mixins import ReprMixin

user_roles = sa.Table(
    "user_roles",
    Base.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), primary_key=True),
)


class User(Base, ReprMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer(), primary_key=True)
    tg_id = sa.Column(sa.Integer(), unique=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy='selectin')

    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)

    def add_role(self, role: "Role"):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: "Role"):
        if role in self.roles:
            self.roles.remove(role)


class Role(Base):
    __tablename__ = "roles"

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(256), unique=True)
    users = relationship("User", secondary=user_roles, back_populates="roles")
