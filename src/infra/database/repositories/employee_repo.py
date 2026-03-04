from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import Employee
from domain.repositories import AbstractEmployeeRepository
from infra.database.models import EmployeeORM


class EmployeeRepository(AbstractEmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, employee_id: int) -> bool:
        result = await self.session.execute(
            select(EmployeeORM.id).where(EmployeeORM.id == employee_id)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, entity: Employee) -> Employee:
        employee_orm = EmployeeORM.from_entity(entity)  # создаём ORM объект
        self.session.add(employee_orm)
        await self.session.flush()
        return employee_orm.to_entity()

    async def get_by_id(self, employee_id: int) -> Employee | None:
        result = await self.session.execute(
            select(EmployeeORM).where(EmployeeORM.id == employee_id)
        )
        model = result.scalar_one_or_none()
        await self.session.flush()
        return model.to_entity() if model else None

    async def update(self, entity: Employee) -> Employee | None:
        result = await self.session.execute(
            update(EmployeeORM)
            .where(EmployeeORM.id == entity.id)
            .values(
                full_name=entity.full_name,
                position=entity.position,
                hired_at=entity.hired_at,
                department_id=entity.department_id,
            )
            .returning(EmployeeORM)
        )
        model = result.scalar_one_or_none()
        await self.session.flush()
        return model.to_entity() if model else None

    async def delete(self, employee_id: int):
        await self.session.execute(
            delete(EmployeeORM).where(EmployeeORM.id == employee_id)
        )
        await self.session.flush()
