from datetime import datetime
from domain.entities import Department
from domain.uow import AbstractUnitOfWork
from domain.services.department_service import DepartmentService


class DepartmentHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._service = DepartmentService(uow)

    async def create(self, department_id: int, name: str, parent_id: int | None):
        entity = Department.create(
            id=department_id, name=name, parent_id=parent_id, created_at=datetime.now()
        )
        return await self._service.create(entity)

    async def get(self, department_id: int):
        return await self._service.get_by_id(department_id)

    async def change(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ):
        return await self._service.change_department(
            department_id=department_id,
            name=name,
            parent_id=parent_id,
        )

    async def update(self, department_id: int, name: str, parent_id: int | None):
        entity = Department.create(
            id=department_id, name=name, parent_id=parent_id, created_at=datetime.now()
        )
        return await self._service.update(entity)

    async def delete(self, department_id: int):
        await self._service.delete(department_id)
