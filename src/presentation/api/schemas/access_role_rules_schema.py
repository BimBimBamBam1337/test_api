from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from domain.models import AccessRoleRuleDomain, Role


class AccessRoleRuleResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор правила", examples=[1])
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
        description="Комментарий к правилу", examples=["Полный доступ к пользователям"]
    )
    created_at: datetime = Field(description="Дата создания правила")
    updated_at: datetime = Field(description="Дата обновления правила")

    @classmethod
    def from_domain(
        cls, access_role_rules: AccessRoleRuleDomain
    ) -> "AccessRoleRuleResponse":
        return cls(
            id=access_role_rules.id,
            role=access_role_rules.role,
            element_id=access_role_rules.element_id,
            read_permission=access_role_rules.read_permission,
            read_all_permission=access_role_rules.read_all_permission,
            create_permission=access_role_rules.create_permission,
            update_permission=access_role_rules.update_permission,
            update_all_permission=access_role_rules.update_all_permission,
            delete_permission=access_role_rules.delete_permission,
            delete_all_permission=access_role_rules.delete_all_permission,
            comment=access_role_rules.comment,
            created_at=access_role_rules.created_at,
            updated_at=access_role_rules.updated_at,
        )


class CreateAccessRoleRuleRequest(BaseModel):
    role: Role = Field(
        description="Роль, которой принадлежит правило", examples=[Role.MANAGER]
    )
    element_id: int = Field(description="ID бизнес-элемента (ресурса)", examples=[3])
    read_permission: bool = Field(
        default=False,
        description="Разрешение на чтение своих объектов",
        examples=[True],
    )
    read_all_permission: bool = Field(
        default=False, description="Разрешение на чтение всех объектов", examples=[True]
    )
    create_permission: bool = Field(
        default=False, description="Разрешение на создание объектов", examples=[True]
    )
    update_permission: bool = Field(
        default=False,
        description="Разрешение на обновление своих объектов",
        examples=[True],
    )
    update_all_permission: bool = Field(
        default=False,
        description="Разрешение на обновление любых объектов",
        examples=[False],
    )
    delete_permission: bool = Field(
        default=False,
        description="Разрешение на удаление своих объектов",
        examples=[False],
    )
    delete_all_permission: bool = Field(
        default=False,
        description="Разрешение на удаление любых объектов",
        examples=[False],
    )
    comment: str | None = Field(
        default=None,
        description="Комментарий к правилу",
        examples=["Полный доступ к пользователям"],
    )


class UpdateAccessRoleRuleRequest(BaseModel):
    read_permission: bool | None = Field(
        default=None, description="Разрешение на чтение своих объектов"
    )
    read_all_permission: bool | None = Field(
        default=None, description="Разрешение на чтение всех объектов"
    )
    create_permission: bool | None = Field(
        default=None, description="Разрешение на создание объектов"
    )
    update_permission: bool | None = Field(
        default=None, description="Разрешение на обновление своих объектов"
    )
    update_all_permission: bool | None = Field(
        default=None, description="Разрешение на обновление любых объектов"
    )
    delete_permission: bool | None = Field(
        default=None, description="Разрешение на удаление своих объектов"
    )
    delete_all_permission: bool | None = Field(
        default=None, description="Разрешение на удаление любых объектов"
    )
    comment: str | None = Field(default=None, description="Комментарий к правилу")

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValidationError("At least one field must be provided for update")
        return values
