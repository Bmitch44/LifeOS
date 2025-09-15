from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from pydantic import ConfigDict


if TYPE_CHECKING:
    from app.modules.school.courses.models import Course


class Assesment(SQLModel, table=True):
    __tablename__ = "assesment"
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    name: str
    description: str
    type: str
    start_date: datetime
    end_date: datetime
    weight: float
    final_grade: float
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})

    course: Optional["Course"] = Relationship(
        back_populates="assesments",
        sa_relationship={"argument": "course"}
    )