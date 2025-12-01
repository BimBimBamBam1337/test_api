from datetime import datetime
from enum import Enum

from pydantic import Field

from .domain_model import DomainModel


class BuisnessElements(str, Enum):
    USERS = "users"
    PRODUCTS = "products"
    ORDERS = "orders"
    STORES = "stores"


class BuisnessElementsNames(str, Enum):
    USERS = "Пользователи"
    PRODUCTS = "Продукты"
    ORDERS = "Заказы"
    STORES = "Магазин"


class BuisnessDomain(DomainModel):
    id: int = Field(description="Уникальный индефикатор правила", examples=[1])
    buisness_elements: BuisnessElements = Field(
        description="Список бизнес элементов", examples=[BuisnessElements.ORDERS]
    )
    name: str = Field(description="Человекочитаемого названия ресурса", examples=[1])
    comment: str | None = Field(
        default=None,
        description="Комментарий к правилу",
        examples=["Полный доступ к пользователям"],
    )
