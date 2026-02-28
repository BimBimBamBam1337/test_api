from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

__all__ = ["SessionFactory", "engine"]


engine = create_async_engine(
    settings.postgres_dsn,
)


SessionFactory = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)
