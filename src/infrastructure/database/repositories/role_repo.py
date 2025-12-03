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
        self, *, id: int, name: str, description: str | None = None
    ) -> RoleDomain:
        role = RoleORM(id=id, name=name, description=description)
        self.session.add(role)
        await self.session.flush()
        return role.to_domain()

    async def get_by_id(self, id: int) -> RoleDomain | None:
        role: RoleORM | None = await self.session.get(RoleORM, id)
        return role.to_domain() if role else None

    async def get_by_name(self, name: str) -> RoleDomain | None:
        result = await self.session.execute(
            select(RoleORM).where(RoleORM.name == name).limit(1)
        )
        role: RoleORM | None = result.scalar_one_or_none()
        return role.to_domain() if role else None

    async def update(
        self,
        id: int,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> RoleDomain | None:
        values = {}
        if name is not None:
            values["name"] = name
        if description is not None:
            values["description"] = description

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
