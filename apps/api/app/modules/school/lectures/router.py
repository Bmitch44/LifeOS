from fastapi import APIRouter, Depends, Query
from app.modules.school.lectures.schemas import LectureCreate, LectureUpdate, PaginatedLectures
from app.modules.school.lectures.service import LecturesService
from app.deps import get_lectures_service, get_current_user
from app.db.models import Lecture

router = APIRouter(prefix="/v1/lectures", tags=["lectures"])

@router.get("", response_model=PaginatedLectures)
async def list_lectures(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    svc: LecturesService = Depends(get_lectures_service),
    _=Depends(get_current_user),
):
    return await svc.list_lectures(page, size)

@router.post("", response_model=Lecture, status_code=201)
async def create_lecture(
    payload: LectureCreate,
    svc: LecturesService = Depends(get_lectures_service),
    _=Depends(get_current_user),
):
    return await svc.create_lecture(payload)

@router.get("/{id}", response_model=Lecture)
async def get_lecture(
    id: int,
    svc: LecturesService = Depends(get_lectures_service),
    _=Depends(get_current_user),
):
    return await svc.get_lecture(id)

@router.put("/{id}", response_model=Lecture)
async def update_lecture(
    id: int,
    payload: LectureUpdate,
    svc: LecturesService = Depends(get_lectures_service),
    _=Depends(get_current_user),
):
    return await svc.update_lecture(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_lecture(
    id: int,
    svc: LecturesService = Depends(get_lectures_service),
    _=Depends(get_current_user),
):
    return await svc.delete_lecture(id)