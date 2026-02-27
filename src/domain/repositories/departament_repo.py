from abc import ABC, abstractmethod

from domain.entities import Departament


class AbstractDepartamentRepository(ABC):
    @abstractmethod
    async def exitst(self, departament_id: int) -> bool:
        raise NotImplemented

    @abstractmethod
    async def create(self, entity: Departament) -> Departament:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, departament_id: int) -> Departament:
        raise NotImplemented

    @abstractmethod
    async def change_departament(
        self,
        departament_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Departament:
        raise NotImplemented

    @abstractmethod
    async def update(self, Departament) -> Departament:
        raise NotImplemented

    @abstractmethod
    async def delete(self, departament_id: int):
        raise NotImplemented
