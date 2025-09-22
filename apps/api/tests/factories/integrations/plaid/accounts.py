from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PlaidAccount


async def create_plaid_account(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    plaid_account_id: str = "acc_1",
    name: Optional[str] = "Checking",
    official_name: Optional[str] = "Official Checking",
    type: Optional[str] = "depository",
    subtype: Optional[str] = "checking",
    current_balance: Optional[float] = 100.0,
    available_balance: Optional[float] = 80.0,
    iso_currency_code: Optional[str] = "USD",
    mask: Optional[str] = "1234",
) -> PlaidAccount:
    acc = PlaidAccount(
        clerk_user_id=clerk_user_id,
        plaid_account_id=plaid_account_id,
        name=name,
        official_name=official_name,
        type=type,
        subtype=subtype,
        current_balance=current_balance,
        available_balance=available_balance,
        iso_currency_code=iso_currency_code,
        mask=mask,
    )
    session.add(acc)
    await session.commit()
    await session.refresh(acc)
    return acc


