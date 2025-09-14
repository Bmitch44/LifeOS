from fastapi import APIRouter, Depends, Query
from app.modules.school.courses.schemas import CourseCreate, CourseUpdate, PaginatedCourses
from app.modules.school.courses.service import CoursesService
from app.deps import get_courses_service, get_current_user
from app.modules.school.courses.models import Course

router = APIRouter(prefix="/v1/courses", tags=["courses"])

@router.get("", response_model=PaginatedCourses)
async def list_courses(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    svc: CoursesService = Depends(get_courses_service),
    _=Depends(get_current_user),
):
    return await svc.list_courses(page, size)

@router.post("", response_model=Course, status_code=201)
async def create_course(
    payload: CourseCreate,
    svc: CoursesService = Depends(get_courses_service),
    _=Depends(get_current_user),
):
    return await svc.create_course(payload)

@router.get("/{id}", response_model=Course)
async def get_course(
    id: int,
    svc: CoursesService = Depends(get_courses_service),
    _=Depends(get_current_user),
):
    return await svc.get_course(id)

@router.put("/{id}", response_model=Course)
async def update_course(
    id: int,
    payload: CourseUpdate,
    svc: CoursesService = Depends(get_courses_service),
    _=Depends(get_current_user),
):
    return await svc.update_course(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_course(
    id: int,
    svc: CoursesService = Depends(get_courses_service),
    _=Depends(get_current_user),
):
    return await svc.delete_course(id)