from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str = Field(nullable=True)
    code: str = Field(unique=True, index=True)
    professor_name: str = Field(nullable=True)
    professor_email: str = Field(nullable=True)
    credits: int = Field(nullable=True)
    semester: str = Field(nullable=True)
    year: int = Field(nullable=True)
    department: str = Field(nullable=True)
    campus: str = Field(nullable=True)
    location: str = Field(nullable=True)
    final_grade: float = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})
    