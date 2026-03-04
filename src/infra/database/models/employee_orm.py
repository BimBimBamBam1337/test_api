from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities import Employee
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .department_orm import DepartmentORM


class EmployeeORM(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    department: Mapped["DepartmentORM"] = relationship(
        "DepartmentORM", back_populates="employees"
    )

    def __repr__(self) -> str:
        return f"<Employee id={self.id} full_name={self.full_name}>"

    @staticmethod
    def from_entity(entity: Employee) -> "EmployeeORM":
        return EmployeeORM(
            id=entity.id,
            department_id=entity.department_id,
            full_name=entity.full_name.strip(),
            position=entity.position.strip(),
            hired_at=entity.hired_at,
        )

    def to_entity(self) -> Employee:
        return Employee(
            id=self.id,
            department_id=self.department_id,
            full_name=self.full_name,
            position=self.position,
            hired_at=self.hired_at,
            created_at=self.created_at,
        )
