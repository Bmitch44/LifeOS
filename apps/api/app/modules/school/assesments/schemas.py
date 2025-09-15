from datetime import datetime
from pydantic import BaseModel
from typing import List
from app.db.models import Assesment


class AssesmentCreate(BaseModel):
    course_id: int
    name: str
    description: str
    type: str
    start_date: datetime
    end_date: datetime
    weight: float
    final_grade: float

class AssesmentUpdate(AssesmentCreate):
    pass

class PaginatedAssesments(BaseModel):
    items: List[Assesment]
    page: int
    size: int
    total: int