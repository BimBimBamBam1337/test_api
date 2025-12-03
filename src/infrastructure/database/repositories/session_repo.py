from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import SessionDomain
from domain.repositories import AbstractSessionRepository
from infrastructure.database.models import SessionORM


class SessionRepository(AbstractSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(
            select(1).where(SessionORM.id == id).limit(1)
        )
        return result.scalar() is not None

    async def create(
        self,
        *,
        id: int,
        user_id: int,
        session_token: str,
        expires_at: datetime,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> SessionDomain:
        session_orm = SessionORM(
            id=id,
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at,
            ip=ip,
            user_agent=user_agent,
        )

        self.session.add(session_orm)
        await self.session.flush()

        return session_orm.to_domain()

    async def get_by_id(self, id: int) -> Optional[SessionDomain]:
        session_orm = await self.session.get(SessionORM, id)
        return session_orm.to_domain() if session_orm else None

    async def get_by_token(self, token: str) -> Optional[SessionDomain]:
        result = await self.session.execute(
            select(SessionORM).where(SessionORM.session_token == token).limit(1)
        )
        session_orm = result.scalar_one_or_none()
        return session_orm.to_domain() if session_orm else None

    async def get_by_user(self, user_id: int) -> list[SessionDomain]:
        result = await self.session.execute(
            select(SessionORM).where(SessionORM.user_id == user_id)
        )
        sessions = result.scalars().all()
        return [s.to_domain() for s in sessions]

    async def update_last_seen(self, id: int):
        await self.session.execute(
            update(SessionORM)
            .where(SessionORM.id == id)
            .values(last_seen_at=datetime.utcnow())
        )
        await self.session.flush()

    async def delete(self, id: int) -> SessionDomain | None:
        result = await self.session.execute(
            delete(SessionORM).where(SessionORM.id == id).returning(SessionORM)
        )

        await self.session.flush()
        session_orm: SessionORM | None = result.scalar_one_or_none()
        return session_orm.to_domain() if session_orm else None

    async def delete_user_sessions(self, user_id: int) -> int:
        result = await self.session.execute(
            delete(SessionORM)
            .where(SessionORM.user_id == user_id)
            .returning(SessionORM.id)
        )
        await self.session.flush()

        deleted = result.scalars().all()
        return len(deleted)

    async def delete_expired(self) -> int:
        now = datetime.utcnow()
        result = await self.session.execute(
            delete(SessionORM)
            .where(SessionORM.expires_at < now)
            .returning(SessionORM.id)
        )
        await self.session.flush()

        deleted = result.scalars().all()
        return len(deleted)
