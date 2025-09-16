from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class PlaidAccount(SQLModel, table=True):
    __tablename__ = "plaid_account"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(unique=True, index=True)
    account_id: str = Field(nullable=True)
    name: str = Field(nullable=True)
    official_name: str = Field(nullable=True)
    type: str = Field(nullable=True)
    subtype: str = Field(nullable=True)
    current_balance: float = Field(nullable=True)
    available_balance: float = Field(nullable=True)
    iso_currency_code: str = Field(nullable=True)
    mask: str = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})