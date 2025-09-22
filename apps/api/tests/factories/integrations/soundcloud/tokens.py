from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SoundcloudToken


async def create_soundcloud_token(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    access_token: Optional[str] = "access",
    token_type: Optional[str] = "bearer",
    expires_in: Optional[int] = 3600,
    refresh_token: Optional[str] = "refresh",
    scope: Optional[str] = "*",
    expires_at: Optional[datetime] = None,
) -> SoundcloudToken:
    obj = SoundcloudToken(
        clerk_user_id=clerk_user_id,
        access_token=access_token,
        token_type=token_type,
        expires_in=expires_in,
        refresh_token=refresh_token,
        scope=scope,
        expires_at=expires_at or (datetime.utcnow() + timedelta(seconds=expires_in)),
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


