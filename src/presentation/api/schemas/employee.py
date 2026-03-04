from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from domain.entities import Employee


class EmployeeResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор сотрудника")

    department_id: int = Field(
        description="Идентификатор подразделения, к которому относится сотрудник"
    )

    full_name: str = Field(
        description="Полное имя сотрудника", min_length=1, max_length=200
    )

    position: str = Field(
        description="Должность сотрудника", min_length=1, max_length=200
    )

    hired_at: datetime | None = Field(default=None, description="Дата приёма на работу")

    created_at: datetime = Field(description="Дата создания записи о сотруднике")

    @classmethod
    def from_domain(cls, entity: Employee) -> "EmployeeResponse":
        return cls(
            id=entity.id,
            department_id=entity.department_id,
            full_name=entity.full_name,
            position=entity.position,
            hired_at=entity.hired_at,
            created_at=entity.created_at,
        )


class CreateEmployeeRequest(BaseModel):
    department_id: int = Field(description="Идентификатор существующего подразделения")

    full_name: str = Field(
        description="Полное имя сотрудника (1–200 символов)",
        min_length=1,
        max_length=200,
    )

    position: str = Field(
        description="Должность сотрудника (1–200 символов)",
        min_length=1,
        max_length=200,
    )

    hired_at: datetime | None = Field(
        default=None, description="Дата приёма на работу (опционально)"
    )

    @field_validator("full_name", "position")
    @classmethod
    def validate_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class UpdateEmployeeRequest(BaseModel):
    department_id: int = Field(description="Идентификатор существующего подразделения")

    full_name: str = Field(
        description="Полное имя сотрудника (1–200 символов)",
        min_length=1,
        max_length=200,
    )

    position: str = Field(
        description="Должность сотрудника (1–200 символов)",
        min_length=1,
        max_length=200,
    )

    hired_at: datetime | None = Field(
        default=None, description="Дата приёма на работу (опционально)"
    )

    @field_validator("full_name", "position")
    @classmethod
    def validate_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value
