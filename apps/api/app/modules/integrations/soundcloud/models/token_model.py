from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class SoundcloudToken(SQLModel, table=True):
    __tablename__ = "soundcloud_token"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    access_token: str = Field(nullable=True)
    token_type: str = Field(nullable=True)
    expires_in: int = Field(nullable=True)
    refresh_token: str = Field(nullable=True)
    scope: str = Field(nullable=True)
    expires_at: datetime = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})