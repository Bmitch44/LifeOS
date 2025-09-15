from fastapi import APIRouter, Depends, Query
from app.modules.school.documents.schemas import DocumentCreate, DocumentUpdate, PaginatedDocuments
from app.modules.school.documents.service import DocumentsService
from app.deps import get_documents_service, get_current_user
from app.db.models import Document


router = APIRouter(prefix="/v1/documents", tags=["documents"])


@router.get("", response_model=PaginatedDocuments)
async def list_documents(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    svc: DocumentsService = Depends(get_documents_service),
    _=Depends(get_current_user),
):
    return await svc.list_documents(page, size)


@router.post("", response_model=Document, status_code=201)
async def create_document(
    payload: DocumentCreate,
    svc: DocumentsService = Depends(get_documents_service),
    _=Depends(get_current_user),
):
    return await svc.create_document(payload)


@router.get("/{id}", response_model=Document)
async def get_document(
    id: int,
    svc: DocumentsService = Depends(get_documents_service),
    _=Depends(get_current_user),
):
    return await svc.get_document(id)


@router.put("/{id}", response_model=Document)
async def update_document(
    id: int,
    payload: DocumentUpdate,
    svc: DocumentsService = Depends(get_documents_service),
    _=Depends(get_current_user),
):
    return await svc.update_document(id, payload)


@router.delete("/{id}", response_model=dict)
async def delete_document(
    id: int,
    svc: DocumentsService = Depends(get_documents_service),
    _=Depends(get_current_user),
):
    return await svc.delete_document(id)

