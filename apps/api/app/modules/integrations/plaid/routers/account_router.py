from fastapi import APIRouter, Depends, Query

from app.modules.integrations.plaid.schemas import PlaidAccountCreate, PlaidAccountUpdate, PaginatedPlaidAccounts
from app.modules.integrations.plaid.services import PlaidAccountService
from app.modules.integrations.plaid.deps import get_plaid_account_service
from app.db.models import PlaidAccount

router = APIRouter(prefix="/v1/plaid/accounts", tags=["plaid accounts"])

@router.get("", response_model=PaginatedPlaidAccounts)
async def list_accounts(
    page: int = Query(1),
    size: int = Query(10),
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.list_accounts(page=page, size=size)


@router.post("", response_model=PlaidAccount, status_code=201)
async def create_account(
    payload: PlaidAccountCreate,
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.create_account(payload)

@router.get("/sync", response_model=dict)
async def sync_accounts(
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.sync_accounts()

@router.get("/{id}", response_model=PlaidAccount)
async def get_account(
    id: int,
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.get_account(id)

@router.put("/{id}", response_model=PlaidAccount)
async def update_account(
    id: int,
    payload: PlaidAccountUpdate,
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.update_account(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_account(
    id: int,
    svc: PlaidAccountService = Depends(get_plaid_account_service),
):
    return await svc.delete_account(id)