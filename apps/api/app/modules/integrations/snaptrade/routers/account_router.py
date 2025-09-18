from fastapi import APIRouter, Depends, Query

from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate, PaginatedSnaptradeAccounts
from app.modules.integrations.snaptrade.services import SnaptradeAccountService
from app.modules.integrations.snaptrade.deps import get_snaptrade_account_service
from app.db.models import SnaptradeAccount

router = APIRouter(prefix="/v1/snaptrade/accounts", tags=["snaptrade accounts"])

@router.get("", response_model=PaginatedSnaptradeAccounts)
async def list_accounts(
    page: int = Query(1),
    size: int = Query(10),
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service)
):
    return await svc.list_accounts(page=page, size=size)

@router.post("", response_model=SnaptradeAccount, status_code=201)
async def create_account(
    payload: SnaptradeAccountCreate,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
):
    return await svc.create_account(payload)

@router.get("/sync", response_model=dict)
async def sync_accounts(
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
):
    return await svc.sync_accounts()

@router.get("/{id}", response_model=SnaptradeAccount)
async def get_account(
    id: int,
    refresh: bool = Query(False),
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
):
    if refresh:
        return await svc.sync_accounts()
    return await svc.get_account(id)

@router.put("/{id}", response_model=SnaptradeAccount)
async def update_account(
    id: int,
    payload: SnaptradeAccountUpdate,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
):
    return await svc.update_account(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_account(
    id: int,
    svc: SnaptradeAccountService = Depends(get_snaptrade_account_service),
):
    return await svc.delete_account(id)