from abc import ABC, abstractmethod

from domain.entities import Employee


class AbstractEmployeeRepository(ABC):
    @abstractmethod
    async def exists(self, employee_id: int) -> bool:
        raise NotImplemented

    @abstractmethod
    async def create(self, entity: Employee) -> Employee:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Employee | None:
        raise NotImplemented

    @abstractmethod
    async def update(self, entity: Employee) -> Employee | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, employee_id: int):
        raise NotImplemented
