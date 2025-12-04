from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import RoleDomain
from domain.repositories import AbstractRoleRepository
from infrastructure.database.models import RoleORM


class RoleRepository(AbstractRoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(select(1).where(RoleORM.id == id).limit(1))
        return result.scalar() is not None

    async def create(
        self, *, id: int, role: str, comment: str | None = None
    ) -> RoleDomain:
        role = RoleORM(id=id, role=role, comment=comment)
        self.session.add(role)
        await self.session.flush()
        return role.to_domain()

    async def get_by_id(self, id: int) -> RoleDomain | None:
        role: RoleORM | None = await self.session.get(RoleORM, id)
        return role.to_domain() if role else None

    async def get_by_role_name(self, role_name: str) -> RoleDomain | None:
        result = await self.session.execute(
            select(RoleORM).where(RoleORM.role == role_name).limit(1)
        )
        role: RoleORM | None = result.scalar_one_or_none()
        return role.to_domain() if role else None

    async def update(
        self, id: int, role_name: str | None = None, comment: str | None = None
    ) -> RoleDomain | None:

        values = {}
        if role_name is not None:
            values["role"] = role_name
        if comment is not None:
            values["comment"] = comment

        result = await self.session.execute(
            update(RoleORM).where(RoleORM.id == id).values(**values).returning(RoleORM)
        )
        await self.session.flush()

        role: RoleORM | None = result.scalar_one_or_none()
        return role.to_domain() if role else None

    async def delete(self, id: int) -> RoleDomain | None:
        result = await self.session.execute(
            delete(RoleORM).where(RoleORM.id == id).returning(RoleORM)
        )
        await self.session.flush()

        role: RoleORM | None = result.scalar_one_or_none()
        return role.to_domain() if role else None

    async def get_all(self) -> list[RoleDomain]:
        result = await self.session.execute(select(RoleORM))
        roles = result.scalars().all()
        return [r.to_domain() for r in roles]
