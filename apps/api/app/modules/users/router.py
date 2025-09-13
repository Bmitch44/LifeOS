from fastapi import APIRouter, Depends, Query

from app.modules.users.schemas import PaginatedUsers, UserCreate, UserOut, UserUpdate
from app.modules.users.service import UsersService
from app.deps import get_current_user, get_users_service


router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("", response_model=PaginatedUsers)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    svc: UsersService = Depends(get_users_service),
    _=Depends(get_current_user),
):
    return await svc.list_users(page, size)


@router.post("", response_model=UserOut, status_code=201)
async def create_user(
    payload: UserCreate,
    svc: UsersService = Depends(get_users_service),
    _=Depends(get_current_user),
):
    return await svc.create_user(payload)


@router.get("/{id}", response_model=UserOut)
async def get_user(
    id: int,
    svc: UsersService = Depends(get_users_service),
    _=Depends(get_current_user),
):
    return await svc.get_user(id)

@router.put("/{id}", response_model=UserOut)
async def update_user(
    id: int,
    payload: UserUpdate,
    svc: UsersService = Depends(get_users_service),
    _=Depends(get_current_user),
):
    return await svc.update_user(id, payload)

@router.delete("/{id}", response_model=UserOut)
async def delete_user(
    id: int,
    svc: UsersService = Depends(get_users_service),
    _=Depends(get_current_user),
):
    return await svc.delete_user(id)

