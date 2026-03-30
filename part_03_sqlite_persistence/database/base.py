"""Part 3 — Async SQLAlchemy engine and session for this part."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from shared.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
    connect_args={"check_same_thread": False},
    # StaticPool keeps a single connection open (good for SQLite in tests)
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_tables() -> None:
    from part_03_sqlite_persistence.database.models import PatientORM, DoctorORM, AppointmentORM
    from shared.database.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
