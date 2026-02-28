from abc import ABC, abstractmethod

from domain.repositories import (
    AbstractDepartmentRepository,
    AbstractEmployeeRepository,
)

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(ABC):
    department_repo: AbstractDepartmentRepository
    employee_repo: AbstractEmployeeRepository

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
