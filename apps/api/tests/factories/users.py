from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def create_user(
    session: AsyncSession,
    *,
    clerk_user_id: str = "user_1",
    email: str = "user1@example.com",
    first_name: Optional[str] = "Test",
    last_name: Optional[str] = "User",
    phone: Optional[str] = None,
) -> User:
    user = User(
        clerk_user_id=clerk_user_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


