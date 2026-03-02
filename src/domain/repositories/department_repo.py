from abc import ABC, abstractmethod

from domain.entities import Department


class AbstractDepartmentRepository(ABC):
    @abstractmethod
    async def exists(self, department_id: int) -> bool:
        raise NotImplemented

    @abstractmethod
    async def create(self, entity: Department) -> Department:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, department_id: int) -> Department | None:
        raise NotImplemented

    @abstractmethod
    async def change_department(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Department | None:
        raise NotImplemented

    @abstractmethod
    async def update(self, entity: Department) -> Department | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, department_id: int):
        raise NotImplemented
