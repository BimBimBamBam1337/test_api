from dataclasses import dataclass
from datetime import datetime


@dataclass
class Departament:
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    @classmethod
    def create(
        cls, id: int, name: str, parent_id: int | None, created_at: datetime
    ) -> "Departament":
        return cls(
            id=id,
            name=name,
            parent_id=parent_id,
            created_at=created_at,
        )
