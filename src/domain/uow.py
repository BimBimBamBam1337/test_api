from abc import ABC, abstractmethod

from domain.repositories import (
    AbstractDepartamentRepository,
    AbstractEmployeRepository,
)

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(ABC):
    departament_repo: AbstractDepartamentRepository
    employe_repo: AbstractEmployeRepository


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
