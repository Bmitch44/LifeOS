from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.school.assesments.repo import AssesmentsRepo
from app.modules.school.assesments.schemas import AssesmentCreate, PaginatedAssesments, AssesmentUpdate
from app.db.models import Assesment


class AssesmentsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AssesmentsRepo(session)

    async def list_assesments(self, page: int, size: int) -> PaginatedAssesments:
        return await self.repo.paginate(page, size)

    async def create_assesment(self, payload: AssesmentCreate) -> Assesment:
        return await self.repo.create(payload)

    async def get_assesment(self, id: int) -> Assesment:
        return await self.repo.get(id)

    async def update_assesment(self, id: int, payload: AssesmentUpdate) -> Assesment:
        return await self.repo.update(id, payload)

    async def delete_assesment(self, id: int) -> dict:
        return await self.repo.delete(id)