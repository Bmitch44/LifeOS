from fastapi import HTTPException
from app.modules.school.lectures.schemas import PaginatedLectures, LectureUpdate, LectureCreate
from app.db.models import Lecture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete


class LecturesRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedLectures:
        try:
            # Calculate offset for pagination
            offset = (page - 1) * size
            
            # Get total count for pagination metadata (SQLAlchemy 2.x)
            total_query = select(func.count()).select_from(Lecture)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            
            # Fetch only the users for the current page
            lectures_query = select(Lecture).offset(offset).limit(size)
            lectures_result = await self.session.execute(lectures_query)
            lectures = lectures_result.scalars().all()
            
            return PaginatedLectures(items=lectures, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: LectureCreate) -> Lecture:
        try:
            lecture = Lecture(
                course_id=payload.course_id,
                name=payload.name,
                description=payload.description,
                start_date=payload.start_date,
                end_date=payload.end_date
            )
            self.session.add(lecture)
            await self.session.commit()
            await self.session.refresh(lecture)
            return lecture
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> Lecture:
        try:
            lecture = await self.session.get(Lecture, id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Lecture not found")
            return lecture
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: LectureUpdate) -> Lecture:
        try:
            lecture = await self.session.get(Lecture, id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Lecture not found")
            lecture.course_id = payload.course_id
            lecture.name = payload.name
            lecture.description = payload.description
            lecture.start_date = payload.start_date
            lecture.end_date = payload.end_date
            await self.session.commit()
            await self.session.refresh(lecture)
            return lecture
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            lecture = await self.session.get(Lecture, id)
            if not lecture:
                raise HTTPException(status_code=404, detail="Lecture not found")
            await self.session.execute(delete(Lecture).where(Lecture.id == id))
            await self.session.commit()
            return {"message": "Lecture deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e


