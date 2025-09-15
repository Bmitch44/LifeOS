from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class Document(SQLModel, table=True):
    __tablename__ = "document"
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(nullable=True)
    file_url: str
    file_type: str = Field(nullable=True)
    size: int = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})

