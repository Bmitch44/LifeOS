from fastapi import APIRouter, Depends, Query

from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate
from app.modules.integrations.snaptrade.services import SnaptradeAccountService
from app.deps import get_current_user, get_snaptrade_account_service
from app.db.models import SnaptradeAccount
from app.core.auth import AuthenticatedUser

router = APIRouter(prefix="/v1/snaptrade/accounts", tags=["snaptrade accounts"])

@router.post("", response_model=SnaptradeAccount, status_code=201)
async def create_account(
    payload: SnaptradeAccountCreate,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
    _=Depends(get_current_user),
):
    return await svc.create_account(payload)

@router.get("/{id}", response_model=SnaptradeAccount)
async def get_account(
    id: int,
    refresh: bool = Query(False),
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    if refresh:
        return await svc.sync_accounts(auth_user.user_id)
    return await svc.get_account(id)

@router.put("/{id}", response_model=SnaptradeAccount)
async def update_account(
    id: int,
    payload: SnaptradeAccountUpdate,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
    _=Depends(get_current_user),
):
    return await svc.update_account(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_account(
    id: int,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
    _=Depends(get_current_user),
):
    return await svc.delete_account(id)

@router.get("/sync", response_model=dict)
async def sync_accounts(
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.sync_accounts(auth_user.user_id)