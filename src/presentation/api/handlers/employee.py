from loguru import logger

from datetime import datetime
from domain.entities import Employee
from domain.uow import AbstractUnitOfWork
from domain.services.employee_service import EmployeeService
from presentation.api.schemas import EmployeeResponse


class EmployeeHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._service = EmployeeService(uow)

    async def create(
        self,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: str | None = None,
    ):
        logger.info(
            "Creating employee full_name='{}', position='{}', department_id={}, hired_at={}",
            full_name,
            position,
            department_id,
            hired_at,
        )

        entity = Employee.create(
            department_id=department_id,
            full_name=full_name.strip(),
            position=position.strip(),
            hired_at=hired_at,
        )

        result = await self._service.create(entity)
        logger.success("Employee created successfully: {}", result)
        return EmployeeResponse.from_domain(result)

    async def get(self, employee_id: int):
        logger.info("Fetching employee with id={}", employee_id)
        result = await self._service.get_by_id(employee_id)
        if result:
            logger.success("Employee fetched successfully: {}", result)
        else:
            logger.warning("Employee with id={} not found", employee_id)
        return result

    async def update(
        self,
        employee_id: int,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: str | None = None,
    ):

        logger.info(
            "Updating employee id={} full_name='{}', position='{}', department_id={}, hired_at={}",
            employee_id,
            full_name,
            position,
            department_id,
            hired_at,
        )

        hired_dt = None
        if hired_at:
            hired_dt = datetime.fromisoformat(hired_at)

        employee = Employee(
            id=employee_id,
            department_id=department_id,
            full_name=full_name.strip(),
            position=position.strip(),
            hired_at=hired_dt,
        )

        result = await self._service.update(employee)
        logger.success("Employee updated successfully: {}", result)
        return EmployeeResponse.from_domain(result)

    async def delete(self, employee_id: int):
        logger.info("Deleting employee with id={}", employee_id)
        await self._service.delete(employee_id)
        logger.success("Employee id={} deleted successfully", employee_id)
