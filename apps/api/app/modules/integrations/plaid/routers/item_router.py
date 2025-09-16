from fastapi import APIRouter, Depends, Query

from app.modules.integrations.plaid.schemas import PlaidItemCreate, PlaidItemUpdate
from app.modules.integrations.plaid.services import PlaidItemService
from app.deps import get_current_user, get_plaid_item_service
from app.db.models import PlaidItem
from app.core.auth import AuthenticatedUser

router = APIRouter(prefix="/v1/plaid/items", tags=["plaid items"])

@router.post("", response_model=PlaidItem, status_code=201)
async def create_item(
    payload: PlaidItemCreate,
    svc: PlaidItemService = Depends(get_plaid_item_service),
    _=Depends(get_current_user),
):
    return await svc.create_item(payload)

@router.get("/sync", response_model=dict)
async def sync_items(
    svc: PlaidItemService = Depends(get_plaid_item_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.sync_items(auth_user.user_id)

@router.get("/{id}", response_model=PlaidItem)
async def get_item(
    id: int,
    refresh: bool = Query(False),
    svc: PlaidItemService = Depends(get_plaid_item_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    if refresh:
        return await svc.sync_items(auth_user.user_id)
    return await svc.get_item(id)

@router.put("/{id}", response_model=PlaidItem)
async def update_item(
    id: int,
    payload: PlaidItemUpdate,
    svc: PlaidItemService = Depends(get_plaid_item_service),
    _=Depends(get_current_user),
):
    return await svc.update_item(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_item(
    id: int,
    svc: PlaidItemService = Depends(get_plaid_item_service),
    _=Depends(get_current_user),
):
    return await svc.delete_item(id)