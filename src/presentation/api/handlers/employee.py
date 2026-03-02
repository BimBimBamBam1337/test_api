from datetime import datetime
from domain.entities import Employee
from domain.uow import AbstractUnitOfWork
from domain.services.employee_service import EmployeeService


class EmployeeHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._service = EmployeeService(uow)

    async def create(
        self,
        employee_id: int,
        department_id: int,
        full_name: str,
        position: str,
    ):
        entity = Employee.create(
            id=employee_id,
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=None,
            created_at=datetime.now(),
        )
        return await self._service.create(entity)

    async def get(self, employee_id: int):
        return await self._service.get_by_id(employee_id)

    async def update(
        self,
        employee_id: int,
        department_id: int,
        full_name: str,
        position: str,
    ):
        entity = Employee.create(
            id=employee_id,
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=None,
            created_at=datetime.now(),
        )
        return await self._service.update(entity)

    async def delete(self, employee_id: int):
        await self._service.delete(employee_id)
