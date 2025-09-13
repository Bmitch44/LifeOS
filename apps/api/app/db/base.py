from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from app.db import models  # noqa: F401  # ensure models imported for metadata

from app.settings import settings


def _get_database_url() -> str:
    if settings.database_url:
        url = settings.database_url
    else:
        # sensible default for local dev; replace with your Neon URL
        url = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    # Ensure async driver
    if url.startswith("postgresql+"):
        fixed = url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    fixed = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Normalize query params for asyncpg (it doesn't accept sslmode/channel_binding)
    try:
        parsed = urlparse(fixed)
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        if "sslmode" in query:
            # asyncpg expects `ssl=true` (or an SSLContext); map require->true
            query.pop("sslmode", None)
            query["ssl"] = "true"
        # drop libpq-specific params
        query.pop("channel_binding", None)
        fixed = urlunparse(
            parsed._replace(query=urlencode(query))  # type: ignore[attr-defined]
        )
    except Exception:
        pass

    return fixed


engine: AsyncEngine = create_async_engine(_get_database_url(), echo=False, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    session: AsyncSession = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)



