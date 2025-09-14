
from pydantic import BaseModel
from typing import List
from app.modules.school.courses.models import Course


class CourseCreate(BaseModel):
    name: str
    description: str
    code: str
    professor_name: str
    professor_email: str
    credits: int
    semester: str
    year: int
    department: str
    campus: str
    location: str
    final_grade: float

class CourseUpdate(CourseCreate):
    pass

class PaginatedCourses(BaseModel):
    items: List[Course]
    page: int
    size: int
    total: int