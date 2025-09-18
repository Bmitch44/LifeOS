from fastapi import APIRouter, Depends, Query

from app.modules.finances.schemas import FinancialAccountCreate, FinancialAccountUpdate, PaginatedFinancialAccounts
from app.modules.finances.services import FinancialAccountService
from app.modules.finances.deps import get_financial_account_service
from app.db.models import FinancialAccount
from app.core.auth import AuthenticatedUser

router = APIRouter(prefix="/v1/finances/accounts", tags=["financial accounts"])

@router.get("", response_model=PaginatedFinancialAccounts)
async def list_financial_accounts(
    page: int = Query(1),
    size: int = Query(10),
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    return await svc.list_financial_accounts(page=page, size=size)

@router.post("", response_model=FinancialAccount)
async def create_financial_account(
    payload: FinancialAccountCreate,
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    return await svc.create_financial_account(payload)

@router.get("/sync", response_model=dict)
async def sync_financial_accounts(
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    return await svc.sync_financial_accounts()

@router.get("/{id}", response_model=FinancialAccount)
async def get_financial_account(
    id: int,
    refresh: bool = Query(False),
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    if refresh:
        return await svc.sync_financial_accounts()
    return await svc.get_financial_account(id)

@router.put("/{id}", response_model=FinancialAccount)
async def update_financial_account(
    id: int,
    payload: FinancialAccountUpdate,
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    return await svc.update_financial_account(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_financial_account(
    id: int,
    svc: FinancialAccountService = Depends(get_financial_account_service),
):
    return await svc.delete_financial_account(id)