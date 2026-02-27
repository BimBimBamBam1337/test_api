from abc import ABC, abstractmethod

from domain.entities import Employe


class AbstractEmployeRepository(ABC):
    @abstractmethod
    async def exitst(self, employe_id: int) -> bool:
        raise NotImplemented

    @abstractmethod
    async def create(self, entity: Employe) -> Employe:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, employe_id: int) -> Employe:
        raise NotImplemented

    @abstractmethod
    async def update(self, Employe) -> Employe:
        raise NotImplemented

    @abstractmethod
    async def delete(self, employe_id: int):
        raise NotImplemented
