from pydantic import BaseModel, Field, ValidationError, model_validator
from domain.models import RoleDomain


class RoleResponse(BaseModel):
    id: int = Field(
        description="Уникальный идентификатор роли",
        examples=[1],
    )
    role: str = Field(
        description="Название роли",
        examples=["admin", "manager"],
    )
    comment: str | None = Field(
        default=None,
        description="Описание роли",
        examples=["Администратор с полными правами"],
    )

    @classmethod
    def from_domain(cls, role: RoleDomain) -> "RoleResponse":
        return cls(
            id=role.id,
            role=role.role,
            comment=role.comment,
        )


class ListRoleResponse(BaseModel):
    roles: list[RoleResponse] = Field(..., description="Список ролей")
    total: int = Field(..., description="Количество ролей")

    @classmethod
    def from_domain(cls, roles: list[RoleDomain]) -> "ListRoleResponse":
        return cls(
            roles=[RoleResponse.from_domain(role) for role in roles],
            total=len(roles),
        )


class CreateRoleRequest(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор роли",
        examples=[1],
    )
    role: str = Field(
        ...,
        description="Название роли",
        examples=["admin"],
    )
    comment: str | None = Field(
        default=None,
        description="Описание роли",
        examples=["Администратор"],
    )


class UpdateRoleRequest(BaseModel):
    role: str | None = Field(
        default=None,
        description="Новое название роли",
        examples=["administrator"],
    )
    comment: str | None = Field(
        default=None,
        description="Новое описание роли",
        examples=["Полный доступ"],
    )

    @model_validator(mode="after")
    def validate_params(self):
        if self.role is None and self.comment is None:
            raise ValidationError(
                "At least one of name or description must be provided"
            )
        return self
