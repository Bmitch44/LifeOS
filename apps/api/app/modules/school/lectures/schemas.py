from datetime import datetime
from pydantic import BaseModel
from typing import List
from app.db.models import Lecture


class LectureCreate(BaseModel):
    course_id: int
    name: str
    description: str
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

