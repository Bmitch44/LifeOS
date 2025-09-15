from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from pydantic import ConfigDict

if TYPE_CHECKING:
    from app.modules.school.assesments.models import Assesment


class Course(SQLModel, table=True):
    __tablename__ = "course"
    model_config = ConfigDict(arbitrary_types_allowed=True)
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

    assesments: List["Assesment"] = Relationship(
        back_populates="course",
        sa_relationship={"argument": "assesment"}
    )
    