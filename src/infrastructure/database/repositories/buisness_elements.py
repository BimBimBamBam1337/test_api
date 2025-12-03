from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import BuisnessElementDomain
from domain.repositories import AbstractBusinessElementRepository
from infrastructure.database.models import BuisnessElementORM


class BuisnessElementRepository(AbstractBusinessElementRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(
            select(1).where(BuisnessElementORM.id == id).limit(1)
        )
        return result.scalar() is not None

    async def create(
        self, *, id: int, code: str, name: str, commit: str | None = None
    ) -> BuisnessElementDomain:
        element_orm = BuisnessElementORM(id=id, code=code, name=name, comment=commit)
        self.session.add(element_orm)
        await self.session.flush()
        return element_orm.to_domain()

    async def get_by_id(self, id: int) -> BuisnessElementDomain | None:
        element_orm = await self.session.get(BuisnessElementORM, id)
        return element_orm.to_domain() if element_orm else None

    async def get_by_name(self, code: str) -> BuisnessElementDomain | None:
        result = await self.session.execute(
            select(BuisnessElementORM).where(BuisnessElementORM.code == code).limit(1)
        )
        element_orm: BuisnessElementORM | None = result.scalar_one_or_none()
        return element_orm.to_domain() if element_orm else None

    async def update(
        self,
        id: int,
        *,
        code: str | None = None,
        name: str | None = None,
        commit: str | None = None,
    ) -> BuisnessElementDomain | None:
        values = {}
        if code is not None:
            values["code"] = code
        if name is not None:
            values["name"] = name
        if commit is not None:
            values["comment"] = commit

        result = await self.session.execute(
            update(BuisnessElementORM)
            .where(BuisnessElementORM.id == id)
            .values(**values)
            .returning(BuisnessElementORM)
        )
        await self.session.flush()
        element_orm: BuisnessElementORM | None = result.scalar_one_or_none()
        return element_orm.to_domain() if element_orm else None

    async def delete(self, id: int) -> BuisnessElementDomain | None:
        result = await self.session.execute(
            delete(BuisnessElementORM)
            .where(BuisnessElementORM.id == id)
            .returning(BuisnessElementORM)
        )
        await self.session.flush()
        element_orm: BuisnessElementORM | None = result.scalar_one_or_none()
        return element_orm.to_domain() if element_orm else None

    async def get_all(self) -> list[BuisnessElementDomain]:
        result = await self.session.execute(select(BuisnessElementORM))
        elements_orm = result.scalars().all()
        return [element.to_domain() for element in elements_orm]
