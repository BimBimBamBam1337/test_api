from domain.exceptions import EmployeNotFoundError, EmployeAlreadyExistsError
from domain.entities import Employe
from domain.uow import AbstractUnitOfWork


class EmployeService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__employe_repo = uow.employe_repo
        self.__departament_repo = uow.departament_repo

    async def create(self, entity: Employe) -> Employe:
        exists = await self.__departament_repo.exists(entity.department_id)
        if exists:
            raise EmployeAlreadyExistsError
        employe = await self.__employe_repo.create(entity)
        return employe

    async def get_by_id(self, employe_id: int) -> Employe:
        employe = await self.__employe_repo.get_by_id(employe_id)
        if employe is None:
            raise EmployeNotFoundError
        return employe

    async def update(self, entity: Employe) -> Employe:
        new_employe = await self.__employe_repo.update(entity)
        if new_employe is None:
            raise EmployeNotFoundError
        return new_employe

    async def delete(self, employe_id: int):
        exists = await self.__employe_repo.exists(employe_id)
        if exists is None:
            raise EmployeNotFoundError
        await self.__employe_repo.delete(employe_id)
