from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import UserDomain, Role
from domain.repositories import AbstractUserRepository
from infrastructure.database.models import UserORM


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(select(1).where(UserORM.id == id).limit(1))
        return result.scalar() is not None

    async def create(
        self, *, id: int, username: str, password: str, role: Role, name: str
    ) -> UserDomain:
        user_orm = UserORM(
            id=id, username=username, password=password, role=role.value, name=name
        )
        self.session.add(user_orm)
        await self.session.flush()
        return user_orm.to_domain()

    async def get_by_id(self, id: int) -> UserDomain | None:
        user_orm: UserORM | None = await self.session.get(UserORM, id)
        return user_orm.to_domain() if user_orm else None

    async def get_by_name(self, name: str) -> UserDomain | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.name == name).limit(1)
        )
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def get_by_username(self, username: str) -> UserDomain | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username).limit(1)
        )
        user: UserORM | None = result.scalar_one_or_none()
        return user.to_domain() if user else None

    async def update(
        self,
        id: int,
        *,
        name: str | None = None,
        username: str | None = None,
        password: str | None = None,
        role: Role | None = None,
        is_active: bool | None = None,
    ) -> UserDomain | None:
        values = {}
        if name is not None:
            values["name"] = name
        if username is not None:
            values["username"] = username
        if password is not None:
            values["password"] = password
        if role is not None:
            values["role"] = role.value
        if is_active is not None:
            values["is_active"] = is_active

        result = await self.session.execute(
            update(UserORM).where(UserORM.id == id).values(**values).returning(UserORM)
        )
        await self.session.flush()
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def delete(self, id: int) -> UserDomain | None:
        result = await self.session.execute(
            delete(UserORM).where(UserORM.id == id).returning(UserORM)
        )
        await self.session.flush()
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def get_all(self, by_role: Role | None = None) -> list[UserDomain]:
        query = select(UserORM)
        if by_role is not None:
            query = query.where(UserORM.role == by_role.value)
        result = await self.session.execute(query)
        users_orm = result.scalars().all()
        return [user_orm.to_domain() for user_orm in users_orm]

    async def soft_delete(self, id: int) -> UserDomain | None:
        await self.session.execute(
            update(UserORM).values(is_active=False).where(UserORM.id == id)
        )
        await self.session.flush()

    async def restore(self, id: int) -> UserDomain | None:
        await self.session.execute(
            update(UserORM).values(is_active=True).where(UserORM.id == id)
        )
        await self.session.flush()
