from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SnaptradeConnection


async def create_snaptrade_connection(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    user_secret: Optional[str] = "secret_1",
    snaptrade_connection_id: Optional[str] = "s1",
    brokerage_name: Optional[str] = "Snap Brokerage",
) -> SnaptradeConnection:
    conn = SnaptradeConnection(
        clerk_user_id=clerk_user_id,
        user_secret=user_secret,
        snaptrade_connection_id=snaptrade_connection_id,
        brokerage_name=brokerage_name,
    )
    session.add(conn)
    await session.commit()
    await session.refresh(conn)
    return conn
