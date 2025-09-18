from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class SnaptradeConnection(SQLModel, table=True):
    __tablename__ = "snaptrade_connection"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    user_secret: str = Field(nullable=True)
    connection_id: str = Field(nullable=True)
    brokerage_name: str = Field(nullable=True)
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())