from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from app.db.models import Lecture


class LectureCreate(BaseModel):
    course_id: int
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    start_date: datetime
    end_date: datetime
    weight: float
    final_grade: float


class LectureUpdate(LectureCreate):
    pass


class PaginatedLectures(BaseModel):
    items: List[Lecture]
    page: int
    size: int
    total: int




