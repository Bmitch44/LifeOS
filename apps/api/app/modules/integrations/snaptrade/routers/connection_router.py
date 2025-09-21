from fastapi import APIRouter, Depends, Query

from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate, SnaptradeConnectionUpdate, PaginatedSnaptradeConnections
from app.modules.integrations.snaptrade.services import SnaptradeConnectionService
from app.modules.integrations.snaptrade.deps import get_snaptrade_connection_service
from app.db.models import SnaptradeConnection

router = APIRouter(prefix="/v1/snaptrade/connections", tags=["snaptrade connections"])

@router.get("", response_model=PaginatedSnaptradeConnections)
async def list_connections(
    page: int = Query(1),
    size: int = Query(10),
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.list_connections(page=page, size=size)

@router.post("", response_model=SnaptradeConnection, status_code=201)
async def create_connection(
    payload: SnaptradeConnectionCreate,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.create_connection(payload)

@router.get("/sync", response_model=dict)
async def sync_connections(
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.sync_connections()

@router.get("/{id}", response_model=SnaptradeConnection)
async def get_connection(
    id: int,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.get_connection(id)

@router.put("/{id}", response_model=SnaptradeConnection)
async def update_connection(
    id: int,
    payload: SnaptradeConnectionUpdate,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.update_connection(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_connection(
    id: int,
    svc: SnaptradeConnectionService = Depends(get_snaptrade_connection_service),
):
    return await svc.delete_connection(id)