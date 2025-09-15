from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.school.lectures.repo import LecturesRepo
from app.modules.school.lectures.schemas import LectureCreate, PaginatedLectures, LectureUpdate
from app.db.models import Lecture


class LecturesService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LecturesRepo(session)
        
    async def list_lectures(self, page: int, size: int) -> PaginatedLectures:
        return await self.repo.paginate(page, size)

    async def create_lecture(self, payload: LectureCreate) -> Lecture:
        return await self.repo.create(payload)

    async def get_lecture(self, id: int) -> Lecture:
        return await self.repo.get(id)

    async def update_lecture(self, id: int, payload: LectureUpdate) -> Lecture:
        return await self.repo.update(id, payload)

    async def delete_lecture(self, id: int) -> dict:
        return await self.repo.delete(id)