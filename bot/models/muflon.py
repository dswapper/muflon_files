import sqlalchemy as sa
from sqlalchemy.orm import relationship

from bot.db import Base
from bot.models.mixins import ReprMixin


class Muflon(Base, ReprMixin):
    __tablename__ = "muflons"

    id = sa.Column(sa.Integer(), primary_key=True)
    user_id = sa.Column(sa.ForeignKey("users.id",
                                      ondelete="CASCADE", onupdate="CASCADE"),
                        unique=True,
                        index=True)
    user = relationship("User", back_populates="muflon", lazy="selectin")

    size = sa.Column(sa.Integer(), default=0, server_default="0")
