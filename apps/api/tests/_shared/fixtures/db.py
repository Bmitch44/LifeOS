import os
import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

# Ensure test DB and minimal creds are set before importing app modules
os.environ.setdefault("LIFEOS_DATABASE_URL", "sqlite+aiosqlite://")
os.environ.setdefault("LIFEOS_PLAID_CLIENT_ID", "test")
os.environ.setdefault("LIFEOS_PLAID_SANDBOX_SECRET", "test")

# Import models to populate SQLModel metadata
from app.db import models as _  # noqa: F401


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    return create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )


@pytest.fixture(scope="session")
async def initialized_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest.fixture(scope="session")
def test_session_maker(test_engine):
    return async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db_session(initialized_db, test_session_maker):
    async with test_session_maker() as session:
        async with session.begin():
            yield session
        await session.rollback()