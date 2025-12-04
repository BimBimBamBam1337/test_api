from enum import Enum

from pydantic import Field

from .domain_model import DomainModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class RoleDomain(DomainModel):
    id: int = Field(description="Уникальный индефикатор правила", examples=[1])
    role: Role = Field(
        description="Роль, которой принадлежит правило", examples=[Role.ADMIN]
    )
    comment: str | None = Field(
        default=None,
        description="Комментарий к роли",
    )
