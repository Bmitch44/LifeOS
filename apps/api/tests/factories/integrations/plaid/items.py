from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PlaidItem


async def create_plaid_item(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    item_id: str = "item_1",
    access_token: str = "access_1",
    institution_name: Optional[str] = "Test Institution",
) -> PlaidItem:
    item = PlaidItem(
        clerk_user_id=clerk_user_id,
        item_id=item_id,
        access_token=access_token,
        institution_name=institution_name,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


