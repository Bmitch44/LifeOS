from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SnaptradeAccount


async def create_snaptrade_account(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    snaptrade_account_id: str = "s1",
    connection_id: int = 1,
    name: Optional[str] = "Snap Account",
    number: Optional[str] = "0001",
    institution_name: Optional[str] = "Snap Bank",
    status: Optional[str] = "active",
    type: Optional[str] = "cash",
    current_balance: Optional[float] = 1000.0,
    currency: Optional[str] = "USD",
) -> SnaptradeAccount:
    acc = SnaptradeAccount(
        clerk_user_id=clerk_user_id,
        snaptrade_account_id=snaptrade_account_id,
        connection_id=connection_id,
        name=name,
        number=number,
        institution_name=institution_name,
        status=status,
        type=type,
        current_balance=current_balance,
        currency=currency,
    )
    session.add(acc)
    await session.commit()
    await session.refresh(acc)
    return acc
