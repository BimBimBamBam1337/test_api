from abc import ABC, abstractmethod

from domain.repositories import (
    AbstractUserRepository,
    AbstractSessionRepository,
    AbstractRoleRepository,
    AbstractRefreshTokenRepository,
    AbstractBusinessElementRepository,
    AbstractAccessRoleRuleRepository,
)

__all__ = ["AbstractUnitOfWork"]


class AbstractUnitOfWork(ABC):
    user_repo: AbstractUserRepository
    session_repo: AbstractSessionRepository
    role_repo: AbstractRoleRepository
    refresh_token_repo: AbstractRefreshTokenRepository
    buisness_element_repo: AbstractBusinessElementRepository
    access_role_rules_repo: AbstractAccessRoleRuleRepository

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
