from fastapi import APIRouter, Depends, Query

from .schemas import PaginatedUsers, UserCreate, UserOut
from .service import UsersService
from ...deps import get_current_user, get_users_service


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


