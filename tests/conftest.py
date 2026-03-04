import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from infra.database.models import Base
from config import settings


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(settings.postgres_dsn, echo=False, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def session(engine):
    connection = await engine.connect()

    transaction = await connection.begin()

    async_session = sessionmaker(
        connection,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    session = async_session()

    try:
        yield session
    finally:
        await session.close()

        await transaction.rollback()

        await connection.close()
