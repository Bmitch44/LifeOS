from __future__ import annotations

from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Assesment
from .courses import create_course


async def create_assesment(
    session: AsyncSession,
    *,
    course_id: int | None = None,
    name: str = "Assesment 1",
    description: str = "Desc",
    type: str = "exam",
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    weight: float = 0.4,
    final_grade: float = 0.0,
) -> Assesment:
    if course_id is None:
        course = await create_course(session)
        course_id = course.id
    now = datetime.now()
    a = Assesment(
        course_id=course_id,
        name=name,
        description=description,
        type=type,
        start_date=start_date or now,
        end_date=end_date or (now + timedelta(hours=1)),
        weight=weight,
        final_grade=final_grade,
    )
    session.add(a)
    await session.commit()
    await session.refresh(a)
    return a
