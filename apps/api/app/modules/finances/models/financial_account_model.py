from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class FinancialAccount(SQLModel, table=True):
    __tablename__ = "financial_account"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    type: Optional[str] = Field(nullable=True)  # e.g., bank | brokerage
    name: Optional[str] = Field(nullable=True)
    institution_name: Optional[str] = Field(nullable=True)
    currency: Optional[str] = Field(nullable=True)
    current_balance: Optional[float] = Field(nullable=True)
    source: str = Field(index=True)  # plaid | snaptrade | ...
    source_account_id: str = Field(index=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})


