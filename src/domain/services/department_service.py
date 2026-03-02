from domain.exceptions import DepartmentNotFoundError, DepartmentAlreadyExistsError
from domain.entities import Department
from domain.uow import AbstractUnitOfWork


class DepartmentService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__department_repo = uow.department_repo

    async def create(self, entity: Department) -> Department:
        exists = await self.__department_repo.exists(entity.id)
        if exists:
            raise DepartmentAlreadyExistsError
        department = await self.__department_repo.create(entity)
        return department

    async def get_by_id(self, department_id: int) -> Department:
        department = await self.__department_repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFoundError
        return department

    async def change_department(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Department:
        new_department = await self.__department_repo.change_department(
            department_id=department_id, name=name, parent_id=parent_id
        )
        if new_department is None:
            raise DepartmentNotFoundError
        return new_department

    async def update(self, entity: Department) -> Department:
        new_department = await self.__department_repo.update(entity)
        if new_department is None:
            raise DepartmentNotFoundError
        return new_department

    async def delete(self, department_id: int):
        exists = await self.__department_repo.delete(department_id)
        if exists is None:
            raise DepartmentNotFoundError
        await self.__department_repo.delete(department_id)
