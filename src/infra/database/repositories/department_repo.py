from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Department
from domain.repositories import AbstractDepartmentRepository
from infra.database.models import DepartmentORM


class DepartmentRepository(AbstractDepartmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, department_id: int) -> bool:
        result = await self.session.execute(
            select(1).where(DepartmentORM.id == department_id)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, entity: Department) -> Department:
        self.session.add(DepartmentORM.from_entity(entity))
        return entity

    async def get_by_id(self, department_id: int) -> Department | None:
        result = await self.session.execute(
            select(DepartmentORM).where(DepartmentORM.id == department_id)
        )
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def change_department(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Department | None:

        values: dict = {}

        if name is not None:
            values["name"] = name

        if parent_id is not None:
            values["parent_id"] = parent_id

        if not values:
            return None

        result = await self.session.execute(
            update(DepartmentORM)
            .where(DepartmentORM.id == department_id)
            .values(**values)
            .returning(DepartmentORM)
        )
        department_orm = result.scalar_one_or_none()

        if department_orm is None:
            return None

        return department_orm.to_entity()

    async def update(self, entity: Department) -> Department | None:
        result = await self.session.execute(
            update(DepartmentORM)
            .where(DepartmentORM.id == entity.id)
            .values(
                name=entity.name,
                parent_id=entity.parent_id,
            )
            .returning(DepartmentORM)
        )
        department_orm = result.scalar_one_or_none()

        if department_orm is None:
            return None

        return department_orm.to_entity()

    async def delete(self, department_id: int):
        await self.session.execute(
            delete(DepartmentORM).where(DepartmentORM.id == department_id)
        )
