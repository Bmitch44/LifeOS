from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.modules.school.courses.models import Course


class Lecture(SQLModel, table=True):
    __tablename__ = "lecture"
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    name: str = Field(unique=True, index=True)
    description: str = Field(nullable=True)
    start_date: datetime = Field(nullable=True)
    end_date: datetime = Field(nullable=True)
    weight: float = Field(nullable=True)
    final_grade: float = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})

    course: Optional["Course"] = Relationship(
        back_populates="lectures",
        sa_relationship={"argument": "course"}
    )
