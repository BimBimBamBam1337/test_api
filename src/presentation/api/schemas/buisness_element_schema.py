from pydantic import BaseModel, Field, ValidationError, model_validator
from domain.models import BuisnessElementDomain, BuisnessElements


class BuisnessElementResponse(BaseModel):
    id: int = Field(description="Уникальный идентификатор бизнес-элемента")
    buisness_elements: BuisnessElements = Field(
        description="Тип бизнес-элемента",
        examples=[BuisnessElements.ORDERS],
    )
    name: str = Field(description="Человекочитаемое название ресурса")
    comment: str | None = Field(description="Комментарий к правилу")

    @classmethod
    def from_domain(
        cls, buisness_element: BuisnessElementDomain
    ) -> "BuisnessElementResponse":
        return cls(
            id=buisness_element.id,
            buisness_elements=buisness_element.buisness_elements,
            name=buisness_element.name,
            comment=buisness_element.comment,
        )


class CreateBuisnessElementRequest(BaseModel):
    buisness_elements: BuisnessElements = Field(
        ...,
        description="Тип бизнес-элемента",
        examples=[BuisnessElements.ORDERS],
    )
    name: str = Field(
        ...,
        description="Человекочитаемое название ресурса",
        examples=["Заказы"],
    )
    comment: str | None = Field(
        None,
        description="Комментарий к правилу",
        examples=["Полный доступ к заказам"],
    )


class UpdateBuisnessElementRequest(BaseModel):
    buisness_elements: BuisnessElements | None = Field(
        None,
        description="Новый тип бизнес-элемента",
    )
    name: str | None = Field(
        None,
        description="Новое человекочитаемое название ресурса",
    )
    comment: str | None = Field(
        None,
        description="Новый комментарий к правилу",
    )

    @model_validator(mode="after")
    def validate_params(self):
        if (
            self.buisness_elements is None
            and self.name is None
            and self.comment is None
        ):
            raise ValidationError(
                "At least one of name or description must be provided"
            )
        return self
