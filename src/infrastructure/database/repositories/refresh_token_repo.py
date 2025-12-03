from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import RefreshTokenDomain
from domain.repositories import AbstractRefreshTokenRepository
from infrastructure.database.models import RefreshTokenORM


class RefreshTokenRepository(AbstractRefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(
            select(1).where(RefreshTokenORM.id == id).limit(1)
        )
        return result.scalar() is not None

    async def create(
        self,
        *,
        id: int,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshTokenDomain:
        token = RefreshTokenORM(
            id=id,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked=False,
        )
        self.session.add(token)
        await self.session.flush()
        return token.to_domain()

    async def get_by_id(self, id: int) -> RefreshTokenDomain | None:
        token: RefreshTokenORM | None = await self.session.get(RefreshTokenORM, id)
        return token.to_domain() if token else None

    async def get_by_user(self, user_id: int) -> list[RefreshTokenDomain]:
        result = await self.session.execute(
            select(RefreshTokenORM).where(RefreshTokenORM.user_id == user_id)
        )
        tokens = result.scalars().all()
        return [t.to_domain() for t in tokens]

    async def revoke(self, id: int) -> bool:
        result = await self.session.execute(
            update(RefreshTokenORM)
            .where(RefreshTokenORM.id == id)
            .values(revoked=True)
            .returning(RefreshTokenORM.id)
        )
        await self.session.flush()
        return result.scalar_one_or_none() is not None

    async def revoke_user_tokens(self, user_id: int) -> int:
        result = await self.session.execute(
            update(RefreshTokenORM)
            .where(RefreshTokenORM.user_id == user_id)
            .values(revoked=True)
            .returning(RefreshTokenORM.id)  # <- возвращаем изменённые id
        )
        await self.session.flush()
        updated_ids = result.scalars().all()
        return len(updated_ids)

    async def delete_expired(self) -> int:
        now = datetime.utcnow()
        result = await self.session.execute(
            delete(RefreshTokenORM)
            .where(RefreshTokenORM.expires_at <= now)
            .returning(RefreshTokenORM.id)  # <- возвращаем удалённые id
        )
        await self.session.flush()
        deleted_ids = result.scalars().all()
        return len(deleted_ids)

    async def get_all(self) -> list[RefreshTokenDomain]:
        result = await self.session.execute(select(RefreshTokenORM))
        tokens = result.scalars().all()
        return [t.to_domain() for t in tokens]
