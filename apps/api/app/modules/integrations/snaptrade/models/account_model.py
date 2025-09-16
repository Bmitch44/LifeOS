from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class SnaptradeAccount(SQLModel, table=True):
    __tablename__ = "snaptrade_account"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(unique=True, index=True)
    account_id: str = Field(nullable=True)
    connection_id: str = Field(nullable=True)
    name: str = Field(nullable=True)
    number: str = Field(nullable=True)
    institution_name: str = Field(nullable=True)
    status: str = Field(nullable=True)
    type: str = Field(nullable=True)
    current_balance: float = Field(nullable=True)
    currency: str = Field(nullable=True)
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())