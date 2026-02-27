from domain.exceptions import DepartamentNotFoundError, DepartamentAlreadyExistsError
from domain.entities import Departament
from domain.uow import AbstractUnitOfWork


class DepartamentService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__departament_repo = uow.departament_repo

    async def create(self, entity: Departament) -> Departament:
        exists = await self.__departament_repo.exists(entity.id)
        if exists:
            raise DepartamentAlreadyExistsError
        departament = await self.__departament_repo.create(entity)
        return departament

    async def get_by_id(self, departament_id: int) -> Departament:
        departament = await self.__departament_repo.get_by_id(departament_id)
        if departament_id is None:
            raise DepartamentNotFoundError
        return departament

    async def change_departament(
        self,
        departament_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Departament:
        new_departament = await self.__departament_repo.change_departament(
            departament_id=departament_id, name=name, parent_id=parent_id
        )
        if new_departament is None:
            raise DepartamentNotFoundError
        return new_departament

    async def update(self, entity: Departament) -> Departament:
        new_departament = await self.__departament_repo.update(entity)
        if new_departament is None:
            raise DepartamentNotFoundError
        return new_departament

    async def delete(self, departament_id: int):
        exists = await self.__departament_repo.delete(departament_id)
        if exists is None:
            raise DepartamentNotFoundError
        await self.__departament_repo.delete(departament_id)
