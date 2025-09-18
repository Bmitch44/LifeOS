import os
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# Ensure the `apps/api` directory is on sys.path so `import app` works regardless of CWD
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import create_app
from app.db.base import get_session
from app.core import auth as core_auth
from app import deps as app_deps


# Use an in-memory SQLite database for tests by default to keep things fast and isolated
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    # Always use test URL (defaults to sqlite+aiosqlite:///:memory:) unless explicitly overridden
    test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    try:
        yield test_engine
    finally:
        await test_engine.dispose()


@pytest.fixture()
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with TestSessionLocal() as s:
        # Clean all tables before each test to ensure isolation
        for table in reversed(SQLModel.metadata.sorted_tables):
            await s.execute(delete(table))
        await s.commit()
        yield s


@pytest.fixture()
def app(session: AsyncSession):
    app = create_app()

    # Override DB session dependency to use the test session
    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_session] = _get_test_session

    # Override get_current_user to bypass external JWKS and DB side-effects
    async def _fake_current_user():
        return core_auth.AuthenticatedUser(sub="test", user_id="test_user", email="test@example.com")

    app.dependency_overrides[app_deps.get_current_user] = _fake_current_user  # type: ignore

    return app


@pytest.fixture()
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    headers = {"Authorization": "Bearer test-token"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        yield ac


