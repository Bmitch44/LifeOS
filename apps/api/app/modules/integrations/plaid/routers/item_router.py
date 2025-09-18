from fastapi import APIRouter, Depends, Query

from app.modules.integrations.plaid.schemas import PlaidItemCreate, PlaidItemUpdate, PaginatedPlaidItems
from app.modules.integrations.plaid.services import PlaidItemService
from app.modules.integrations.plaid.deps import get_plaid_item_service
from app.db.models import PlaidItem

router = APIRouter(prefix="/v1/plaid/items", tags=["plaid items"])

@router.get("", response_model=PaginatedPlaidItems)
async def list_items(
    page: int = Query(1),
    size: int = Query(10),
    svc: PlaidItemService = Depends(get_plaid_item_service),
):
    return await svc.list_items(page=page, size=size)

@router.post("", response_model=PlaidItem, status_code=201)
async def create_item(
    payload: PlaidItemCreate,
    svc: PlaidItemService = Depends(get_plaid_item_service),
):
    return await svc.create_item(payload)

@router.get("/sync", response_model=dict)
async def sync_items(
    svc: PlaidItemService = Depends(get_plaid_item_service),
):
    return await svc.sync_items()

@router.get("/{id}", response_model=PlaidItem)
async def get_item(
    id: int,
    refresh: bool = Query(False),
    svc: PlaidItemService = Depends(get_plaid_item_service),
):
    if refresh:
        return await svc.sync_items()
    return await svc.get_item(id)

@router.put("/{id}", response_model=PlaidItem)
async def update_item(
    id: int,
    payload: PlaidItemUpdate,
    svc: PlaidItemService = Depends(get_plaid_item_service)
):
    return await svc.update_item(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_item(
    id: int,
    svc: PlaidItemService = Depends(get_plaid_item_service)
):
    return await svc.delete_item(id)