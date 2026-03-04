from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Department
from domain.repositories import AbstractDepartmentRepository
from infra.database.models import DepartmentORM, EmployeeORM


class DepartmentRepository(AbstractDepartmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, name: str) -> bool:
        result = await self.session.execute(select(1).where(DepartmentORM.name == name))
        return result.scalar_one_or_none() is not None

    async def create(self, entity: Department) -> Department:
        department_orm = DepartmentORM.from_entity(entity)
        self.session.add(department_orm)
        await self.session.flush()
        return department_orm.to_entity()

    async def get_by_id(self, department_id: int) -> Department | None:
        result = await self.session.execute(
            select(DepartmentORM).where(DepartmentORM.id == department_id)
        )
        model = result.scalar_one_or_none()
        await self.session.flush()
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
        await self.session.flush()
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
        await self.session.flush()
        return department_orm.to_entity()

    async def _collect_children_ids(
        self,
        session: AsyncSession,
        department_id: int,
    ) -> list[int]:

        result = await self.session.execute(
            select(DepartmentORM.id).where(DepartmentORM.parent_id == department_id)
        )

        children_ids = [row[0] for row in result.all()]
        all_ids = []

        for child_id in children_ids:
            all_ids.append(child_id)
            nested = await self._collect_children_ids(self.session, child_id)
            all_ids.extend(nested)

        return all_ids

    async def delete(
        self,
        department_id: int,
        mode: str,
        reassign_to_department_id: int | None,
    ) -> None:

        children_ids = await self._collect_children_ids(
            self.session,
            department_id,
        )

        all_ids = [department_id] + children_ids

        if mode == "cascade":

            # удалить сотрудников
            await self.session.execute(
                delete(EmployeeORM).where(EmployeeORM.department_id.in_(all_ids))
            )

            # удалить подразделения
            await self.session.execute(
                delete(DepartmentORM).where(DepartmentORM.id.in_(all_ids))
            )

        elif mode == "reassign":

            await self.session.execute(
                update(EmployeeORM)
                .where(EmployeeORM.department_id.in_(all_ids))
                .values(department_id=reassign_to_department_id)
            )

            # удалить подразделения
            await self.session.execute(
                delete(DepartmentORM).where(DepartmentORM.id.in_(all_ids))
            )
            await self.session.flush()
        else:
            raise ValueError("Invalid delete mode")

    async def get_children(self, parent_id: int):
        result = await self.session.execute(
            select(DepartmentORM).where(DepartmentORM.parent_id == parent_id)
        )
        return result.scalars().all()

    async def get_employees(self, department_id: int):
        result = await self.session.execute(
            select(EmployeeORM).where(EmployeeORM.department_id == department_id)
        )
        return result.scalars().all()
