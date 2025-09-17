from fastapi import APIRouter, Depends, Query

from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate, SnaptradeConnectionUpdate, PaginatedSnaptradeConnections
from app.modules.integrations.snaptrade.services import SnaptradeConnectionService
from app.deps import get_current_user, get_snaptrade_connection_service
from app.db.models import SnaptradeConnection
from app.core.auth import AuthenticatedUser

router = APIRouter(prefix="/v1/snaptrade/connections", tags=["snaptrade connections"])

@router.get("", response_model=PaginatedSnaptradeConnections)
async def list_connections(
    page: int = Query(1),
    size: int = Query(10),
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.list_connections(clerk_user_id=auth_user.user_id, page=page, size=size)

@router.post("", response_model=SnaptradeConnection, status_code=201)
async def create_connection(
    payload: SnaptradeConnectionCreate,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    _=Depends(get_current_user),
):
    return await svc.create_connection(payload)

@router.get("/sync", response_model=dict)
async def sync_connections(
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.sync_connections(auth_user.user_id)

@router.get("/{id}", response_model=SnaptradeConnection)
async def get_connection(
    id: int,
    refresh: bool = Query(False),
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    if refresh:
        return await svc.sync_connections(auth_user.user_id)
    return await svc.get_connection(id)

@router.put("/{id}", response_model=SnaptradeConnection)
async def update_connection(
    id: int,
    payload: SnaptradeConnectionUpdate,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    _=Depends(get_current_user),
):
    return await svc.update_connection(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_connection(
    id: int,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
    _=Depends(get_current_user),
):
    return await svc.delete_connection(id)