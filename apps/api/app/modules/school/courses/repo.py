from fastapi import HTTPException
from app.modules.school.courses.schemas import CourseCreate, PaginatedCourses, CourseUpdate
from app.modules.school.courses.models import Course
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class CoursesRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedCourses:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(Course)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            courses_query = select(Course).offset(offset).limit(size)
            courses_result = await self.session.execute(courses_query)
            courses = courses_result.scalars().all()
            return PaginatedCourses(items=courses, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: CourseCreate) -> Course:
        try:
            course = Course(name=payload.name, description=payload.description, code=payload.code, professor_name=payload.professor_name, professor_email=payload.professor_email, credits=payload.credits, semester=payload.semester, year=payload.year, department=payload.department, campus=payload.campus, location=payload.location, final_grade=payload.final_grade)
            self.session.add(course)
            await self.session.commit()
            await self.session.refresh(course)
            return course
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> Course:
        try:
            course = await self.session.get(Course, id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            return course
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: CourseUpdate) -> Course:
        try:
            course = await self.session.get(Course, id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            course.name = payload.name
            course.description = payload.description
            course.code = payload.code
            course.professor_name = payload.professor_name
            course.professor_email = payload.professor_email
            course.credits = payload.credits
            course.semester = payload.semester
            course.year = payload.year
            course.department = payload.department
            course.campus = payload.campus
            course.location = payload.location
            course.final_grade = payload.final_grade
            await self.session.commit()
            await self.session.refresh(course)
            return course
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            course = await self.session.get(Course, id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            await self.session.delete(course)
            await self.session.commit()
            return {"message": "Course deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e
        