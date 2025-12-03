from sqlalchemy import BIGINT, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.models import BuisnessElementDomain, BuisnessElements
from .base import BaseORM


class BuisnessElementORM(BaseORM):
    __tablename__ = "business_elements"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    buisness_elements: Mapped[BuisnessElements] = mapped_column(
        Enum(BuisnessElements), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"BusinessElementORM(id={self.id!r}, name={self.name!r}, buisness_elements={self.buisness_elements!r})"

    def to_domain(self) -> BuisnessElementDomain:
        return BuisnessElementDomain.model_validate(self)
