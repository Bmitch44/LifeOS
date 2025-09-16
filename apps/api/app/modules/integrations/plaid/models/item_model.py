from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class PlaidItem(SQLModel, table=True):
    __tablename__ = "plaid_item"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(unique=True, index=True)
    item_id: str = Field(nullable=True)
    access_token: str = Field(nullable=True)
    institution_name: str = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})