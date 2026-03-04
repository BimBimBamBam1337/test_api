from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    id: int | None
    department_id: int
    full_name: str
    position: str
    hired_at: datetime | None = None
    created_at: datetime | None = None

    @classmethod
    def create(
        cls,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: datetime | None,
    ) -> "Employee":
        return cls(
            id=None,
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
            created_at=None,
        )
