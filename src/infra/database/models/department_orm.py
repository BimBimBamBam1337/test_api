from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities import Department
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .employee_orm import EmployeeORM


class DepartmentORM(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # родитель
    parent: Mapped[Optional["DepartmentORM"]] = relationship(
        "DepartmentORM",
        remote_side="DepartmentORM.id",
        back_populates="children",
    )

    # дочерние подразделения
    children: Mapped[List["DepartmentORM"]] = relationship(
        "DepartmentORM",
        back_populates="parent",
    )

    # сотрудники
    employees: Mapped[List["EmployeeORM"]] = relationship(
        "EmployeeORM",
        back_populates="department",
    )

    def __repr__(self) -> str:
        return f"<DepartmentORM id={self.id} name={self.name}>"

    @staticmethod
    def from_entity(entity: Department) -> "DepartmentORM":
        return DepartmentORM(
            id=entity.id,
            name=entity.name.strip(),
            parent_id=entity.parent_id,
        )

    def to_entity(self) -> Department:
        return Department(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
            created_at=self.created_at,
        )
