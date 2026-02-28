from domain.exceptions import EmployeeNotFoundError, EmployeeAlreadyExistsError
from domain.entities import Employee
from domain.uow import AbstractUnitOfWork


class EmployeeService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__employe_repo = uow.employe_repo
        self.__departament_repo = uow.departament_repo

    async def create(self, entity: Employee) -> Employee:
        exists = await self.__departament_repo.exists(entity.department_id)
        if exists:
            raise EmployeeAlreadyExistsError
        employe = await self.__employe_repo.create(entity)
        return employe

    async def get_by_id(self, employe_id: int) -> Employee:
        employe = await self.__employe_repo.get_by_id(employe_id)
        if employe is None:
            raise EmployeeNotFoundError
        return employe

    async def update(self, entity: Employee) -> Employee:
        new_employe = await self.__employe_repo.update(entity)
        if new_employe is None:
            raise EmployeeNotFoundError
        return new_employe

    async def delete(self, employe_id: int):
        exists = await self.__employe_repo.exists(employe_id)
        if exists is None:
            raise EmployeeNotFoundError
        await self.__employe_repo.delete(employe_id)
