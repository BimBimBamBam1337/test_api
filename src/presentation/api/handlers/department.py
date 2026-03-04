from loguru import logger

from datetime import datetime
from domain.entities import Department
from domain.uow import AbstractUnitOfWork
from domain.services.department_service import DepartmentService
from presentation.api.schemas import DepartmentResponse


class DepartmentHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow
        self._service = DepartmentService(uow)

    async def create(self, name: str, parent_id: int | None) -> DepartmentResponse:
        logger.info("Creating department with name='{}', parent_id={}", name, parent_id)
        entity = Department.create(name=name, parent_id=parent_id)
        result = await self._service.create(entity)
        logger.success("Department created successfully: {}", result)
        return DepartmentResponse.from_domain(result)

    async def get(self, department_id: int) -> DepartmentResponse:
        logger.info("Fetching department with id={}", department_id)
        result = await self._service.get_by_id(department_id)
        return DepartmentResponse.from_domain(result)

    async def change(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> DepartmentResponse:
        logger.info(
            "Changing department id={} with name='{}', parent_id={}",
            department_id,
            name,
            parent_id,
        )
        result = await self._service.change_department(
            department_id=department_id,
            name=name,
            parent_id=parent_id,
        )
        logger.success("Department changed successfully: {}", result)
        return DepartmentResponse.from_domain(result)

    async def update(
        self, department_id: int, name: str, parent_id: int | None
    ) -> DepartmentResponse:
        logger.info(
            "Updating department id={} with name='{}', parent_id={}",
            department_id,
            name,
            parent_id,
        )
        department = Department(id=department_id, name=name, parent_id=parent_id)
        result = await self._service.update(department)
        logger.success("Department updated successfully: {}", result)
        return DepartmentResponse.from_domain(result)

    async def delete(
        self,
        department_id: int,
        mode: str,
        reassign_to_department_id: int | None,
    ):
        logger.info(
            "Deleting department id={}, mode='{}', reassign_to_department_id={}",
            department_id,
            mode,
            reassign_to_department_id,
        )
        await self._service.delete(
            department_id=department_id,
            mode=mode,
            reassign_to_department_id=reassign_to_department_id,
        )
        logger.success("Department id={} deleted successfully", department_id)

    async def get_tree(
        self, department_id: int, depth: int = 1, include_employees: bool = True
    ):
        logger.info(
            "Fetching department tree id={}, depth={}, include_employees={}",
            department_id,
            depth,
            include_employees,
        )
        tree = await self._service.get_tree(
            department_id=department_id,
            depth=depth,
            include_employees=include_employees,
        )
        logger.success("Department tree fetched successfully for id={}", department_id)
        return tree
