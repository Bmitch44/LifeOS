from fastapi import APIRouter, Depends, Query
from app.modules.school.assesments.schemas import AssesmentCreate, AssesmentUpdate, PaginatedAssesments
from app.modules.school.assesments.service import AssesmentsService
from app.deps import get_assesments_service, get_current_user
from app.db.models import Assesment

router = APIRouter(prefix="/v1/assesments", tags=["assesments"])

@router.get("", response_model=PaginatedAssesments)
async def list_assesments(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    svc: AssesmentsService = Depends(get_assesments_service),
    _=Depends(get_current_user),
):
    return await svc.list_assesments(page, size)

@router.post("", response_model=Assesment, status_code=201) 
async def create_assesment(
    payload: AssesmentCreate,
    svc: AssesmentsService = Depends(get_assesments_service),
    _=Depends(get_current_user),
):
    return await svc.create_assesment(payload)

@router.get("/{id}", response_model=Assesment)
async def get_assesment(
    id: int,
    svc: AssesmentsService = Depends(get_assesments_service),
    _=Depends(get_current_user),
):
    return await svc.get_assesment(id)

@router.put("/{id}", response_model=Assesment)
async def update_assesment(
    id: int,
    payload: AssesmentUpdate,
    svc: AssesmentsService = Depends(get_assesments_service),
    _=Depends(get_current_user),
):
    return await svc.update_assesment(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_assesment(
    id: int,
    svc: AssesmentsService = Depends(get_assesments_service),
    _=Depends(get_current_user),
):
    return await svc.delete_assesment(id)