from datetime import datetime

from sqlalchemy import BIGINT, BOOLEAN, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from domain.models import UserDomain, Role

from .base import BaseORM


class UserORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, server_default=expression.func(False)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"UserORM(id={self.id!r}, name={self.name!r}, username={self.username!r})"
        )

    def to_domain(self) -> UserDomain:
        return UserDomain.model_validate(self)
