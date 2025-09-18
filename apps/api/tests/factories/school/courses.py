from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Course


async def create_course(
    session: AsyncSession,
    *,
    name: str = "Course 1",
    description: str = "Desc",
    code: str = "CSE101",
    professor_name: str = "Prof",
    professor_email: str = "prof@example.com",
    credits: int = 3,
    semester: str = "Fall",
    year: int = 2025,
    department: str = "CS",
    campus: str = "Main",
    location: str = "Bldg A",
    final_grade: float = 0.0,
) -> Course:
    course = Course(
        name=name,
        description=description,
        code=code,
        professor_name=professor_name,
        professor_email=professor_email,
        credits=credits,
        semester=semester,
        year=year,
        department=department,
        campus=campus,
        location=location,
        final_grade=final_grade,
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course
