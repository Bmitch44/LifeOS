from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SnaptradeActivity


async def create_snaptrade_activity(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    account_id: int = 1,
    activity_id: str = "act_1",
    symbol_id: Optional[str] = None,
    option_symbol_id: Optional[str] = None,
    type: Optional[str] = None,
    option_type: Optional[str] = None,
    price: Optional[float] = None,
    units: Optional[float] = None,
    amount: Optional[float] = None,
    description: Optional[str] = None,
    currency: Optional[str] = None,
    fees: Optional[float] = None,
    fx_rate: Optional[float] = None,
    institution: Optional[str] = None,
) -> SnaptradeActivity:
    act = SnaptradeActivity(
        clerk_user_id=clerk_user_id,
        account_id=account_id,
        activity_id=activity_id,
        symbol_id=symbol_id,
        option_symbol_id=option_symbol_id,
        type=type,
        option_type=option_type,
        price=price,
        units=units,
        amount=amount,
        description=description,
        currency=currency,
        fees=fees,
        fx_rate=fx_rate,
        institution=institution,
    )
    session.add(act)
    await session.commit()
    await session.refresh(act)
    return act


