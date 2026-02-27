from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employe:
    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: datetime | None
    created_at: datetime

    @classmethod
    def create(
        cls,
        id: int,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: datetime | None,
        created_at: datetime,
    ) -> "Employe":
        return cls(
            id=id,
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
            created_at=created_at,
        )
