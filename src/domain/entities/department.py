from dataclasses import dataclass
from datetime import datetime


@dataclass
class Department:
    id: int | None
    name: str
    parent_id: int | None
    created_at: datetime | None = None

    @classmethod
    def create(cls, name: str, parent_id: int | None) -> "Department":
        return cls(
            id=None,
            name=name,
            parent_id=parent_id,
            created_at=None,
        )
