from datetime import datetime
from sqlalchemy import BIGINT, BOOLEAN, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.models import AccessRoleRuleDomain, Role
from .base import BaseORM


class AccessRoleRuleORM(BaseORM):
    __tablename__ = "access_role_rules"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    element_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("business_elements.id"), nullable=False
    )

    read_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    read_all_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    create_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    update_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    update_all_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    delete_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    delete_all_permission: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )

    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"AccessRoleRuleORM(id={self.id!r}, role={self.role!r}, element_id={self.element_id!r})"

    def to_domain(self) -> AccessRoleRuleDomain:
        return AccessRoleRuleDomain.model_validate(self)
