from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.school.assesments.schemas import AssesmentCreate, PaginatedAssesments, AssesmentUpdate
from app.db.models import Assesment
from sqlalchemy import select, func


class AssesmentsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedAssesments:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(Assesment)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            assesments_query = select(Assesment).offset(offset).limit(size)
            assesments_result = await self.session.execute(assesments_query)
            assesments = assesments_result.scalars().all()
            return PaginatedAssesments(items=assesments, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: AssesmentCreate) -> Assesment:
        try:
            assesments = Assesment(course_id=payload.course_id, name=payload.name, description=payload.description, type=payload.type, start_date=payload.start_date, end_date=payload.end_date, weight=payload.weight, final_grade=payload.final_grade)
            self.session.add(assesments)
            await self.session.commit()
            await self.session.refresh(assesments)
            return assesments
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> Assesment:
        try:
            assesments = await self.session.get(Assesment, id)
            if not assesments:
                raise HTTPException(status_code=404, detail="Assesment not found")
            return assesments
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: AssesmentUpdate) -> Assesment:
        try:
            assesments = await self.session.get(Assesment, id)
            if not assesments:
                raise HTTPException(status_code=404, detail="Assesment not found")
            assesments.course_id = payload.course_id
            assesments.name = payload.name
            assesments.description = payload.description
            assesments.type = payload.type
            assesments.start_date = payload.start_date
            assesments.end_date = payload.end_date
            assesments.weight = payload.weight
            assesments.final_grade = payload.final_grade
            await self.session.commit()
            await self.session.refresh(assesments)
            return assesments
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            assesments = await self.session.get(Assesment, id)
            if not assesments:
                raise HTTPException(status_code=404, detail="Assesment not found")
            await self.session.delete(assesments)
            await self.session.commit()
            return {"message": "Assesment deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e