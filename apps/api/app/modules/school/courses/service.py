from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.school.courses.repo import CoursesRepo
from app.modules.school.courses.schemas import CourseCreate, PaginatedCourses, CourseUpdate
from app.modules.school.courses.models import Course


class CoursesService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CoursesRepo(session)
        
    async def list_courses(self, page: int, size: int) -> PaginatedCourses:
        return await self.repo.paginate(page, size)

    async def create_course(self, payload: CourseCreate) -> Course:
        return await self.repo.create(payload)

    async def get_course(self, id: int) -> Course:
        return await self.repo.get(id)

    async def update_course(self, id: int, payload: CourseUpdate) -> Course:
        return await self.repo.update(id, payload)

    async def delete_course(self, id: int) -> dict:
        return await self.repo.delete(id)