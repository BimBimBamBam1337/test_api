from sqlalchemy import BIGINT, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from domain.models import RoleDomain, Role
from .base import BaseORM


class RoleORM(BaseORM):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    role: Mapped[Role] = mapped_column(nullable=False)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"RoleORM(id={self.id!r}, role={self.role!r}, comment={self.comment!r})"

    def to_domain(self) -> RoleDomain:
        return RoleDomain.model_validate(self)
