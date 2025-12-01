from datetime import datetime

from pydantic import Field

from .domain_model import DomainModel
from .role_model import Role


class AccessRoleRuleDomain(DomainModel):
    id: int = Field(description="Уникальный индефикатор правила", examples=[1])
    role: Role = Field(
        description="Роль, которой принадлежит правило", examples=[Role.ADMIN]
    )

    element_id: int = Field(description="ID бизнес-элемента (ресурса)", examples=[3])

    read_permission: bool = Field(
        description="Можно ли читать только свои объекты", examples=[True]
    )
    read_all_permission: bool = Field(
        description="Можно ли читать любые объекты", examples=[True]
    )

    create_permission: bool = Field(
        description="Можно ли создавать объекты", examples=[True]
    )

    update_permission: bool = Field(
        description="Можно ли обновлять только свои объекты", examples=[True]
    )
    update_all_permission: bool = Field(
        description="Можно ли обновлять любые объекты", examples=[False]
    )

    delete_permission: bool = Field(
        description="Можно ли удалять только свои объекты", examples=[False]
    )
    delete_all_permission: bool = Field(
        description="Можно ли удалять любые объекты", examples=[False]
    )

    comment: str | None = Field(
        default=None,
        description="Комментарий к правилу",
        examples=["Полный доступ к пользователям"],
    )

    created_at: datetime = Field(description="Дата создания правила")
    updated_at: datetime = Field(description="Дата обновления правила")
