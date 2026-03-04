from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from domain.entities import Department
from .employee import EmployeeResponse


class DepartmentResponse(BaseModel):
    id: int | None = Field(description="Уникальный идентификатор подразделения")

    name: str = Field(
        description="Название подразделения", min_length=1, max_length=200
    )

    parent_id: int | None = Field(
        default=None,
        description="Идентификатор родительского подразделения (null — если корневое)",
    )

    created_at: datetime | None = Field(description="Дата создания подразделения")

    @classmethod
    def from_domain(cls, entity: Department) -> "DepartmentResponse":
        return cls(
            id=entity.id,
            name=entity.name,
            parent_id=entity.parent_id,
            created_at=entity.created_at,
        )


class CreateDepartmentRequest(BaseModel):
    name: str = Field(
        description="Название подразделения (1–200 символов, уникально в пределах одного родителя)",
        min_length=1,
        max_length=200,
    )

    parent_id: int | None = Field(
        default=None,
        description="Идентификатор родительского подразделения (опционально)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class UpdateDepartmentRequest(BaseModel):
    name: str = Field(
        description="Название подразделения (1–200 символов, уникально в пределах одного родителя)",
        min_length=1,
        max_length=200,
    )

    parent_id: int | None = Field(
        default=None, description="Идентификатор родительского подразделения"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class DepartmentTreeResponse(BaseModel):
    id: int = Field(description="ID подразделения")
    name: str = Field(description="Название подразделения")
    parent_id: int | None = Field(description="ID родителя")
    children: list["DepartmentTreeResponse"] = Field(
        default_factory=list, description="Список дочерних подразделений"
    )
    employees: list["EmployeeResponse"] = Field(
        default_factory=list, description="Сотрудники подразделения"
    )
