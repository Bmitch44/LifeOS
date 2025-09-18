from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FinancialAccount


async def create_financial_account(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    type: Optional[str] = "bank",
    name: Optional[str] = "Fin Acc",
    institution_name: Optional[str] = "Inst",
    currency: Optional[str] = "USD",
    current_balance: Optional[float] = 10.0,
    source: str = "plaid",
    source_account_id: str = "src_1",
) -> FinancialAccount:
    acc = FinancialAccount(
        clerk_user_id=clerk_user_id,
        type=type,
        name=name,
        institution_name=institution_name,
        currency=currency,
        current_balance=current_balance,
        source=source,
        source_account_id=source_account_id,
    )
    session.add(acc)
    await session.commit()
    await session.refresh(acc)
    return acc
