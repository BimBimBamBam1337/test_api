from sqlalchemy.ext.asyncio import AsyncSession

from domain.uow import AbstractUnitOfWork
from infrastructure.database.repositories import (
    UserRepository,
    SessionRepository,
    AccessRoleRuleRepository,
    RefreshTokenRepository,
    RoleRepository,
    BuisnessElementRepository,
)


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.user_repo = UserRepository(self.session)
        self.session_repo = SessionRepository(self.session)
        self.role_repo = RoleRepository(self.session)
        self.refresh_token_repo = RefreshTokenRepository(self.session)
        self.buisness_element_repo = BuisnessElementRepository(self.session)
        self.access_role_rules_repo = AccessRoleRuleRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
