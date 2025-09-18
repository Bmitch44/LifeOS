from __future__ import annotations

from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Lecture
from .courses import create_course


async def create_lecture(
    session: AsyncSession,
    *,
    course_id: int | None = None,
    name: str = "Lecture 1",
    description: str = "Desc",
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    weight: float = 0.0,
    final_grade: float = 0.0,
) -> Lecture:
    if course_id is None:
        course = await create_course(session)
        course_id = course.id
    now = datetime.now()
    lecture = Lecture(
        course_id=course_id,
        name=name,
        description=description,
        start_date=start_date or now,
        end_date=end_date or (now + timedelta(hours=1)),
        weight=weight,
        final_grade=final_grade,
    )
    session.add(lecture)
    await session.commit()
    await session.refresh(lecture)
    return lecture
