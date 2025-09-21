from fastapi import APIRouter, Depends, Query

from app.modules.integrations.snaptrade.schemas import SnaptradeActivityCreate, SnaptradeActivityUpdate, PaginatedSnaptradeActivities
from app.modules.integrations.snaptrade.services import SnaptradeActivityService
from app.modules.integrations.snaptrade.deps import get_snaptrade_activity_service
from app.db.models import SnaptradeActivity

router = APIRouter(prefix="/v1/snaptrade/activities", tags=["snaptrade activities"])

@router.get("", response_model=PaginatedSnaptradeActivities)
async def list_activities(
    page: int = Query(1),
    size: int = Query(10),
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service)
):
    return await svc.list_activities(page=page, size=size)

@router.post("", response_model=SnaptradeActivity, status_code=201)
async def create_activity(
    payload: SnaptradeActivityCreate,
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service),
):
    return await svc.create_activity(payload)

@router.get("/sync/{account_id}", response_model=dict)
async def sync_activities(
    account_id: int,
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service),
):
    return await svc.sync_activities(account_id)

@router.get("/{id}", response_model=SnaptradeActivity)
async def get_activity(
    id: int,
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service),
):
    return await svc.get_activity(id)

@router.put("/{id}", response_model=SnaptradeActivity)
async def update_activity(
    id: int,
    payload: SnaptradeActivityUpdate,
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service),
):
    return await svc.update_activity(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_activity(
    id: int,
    svc: SnaptradeActivityService = Depends(get_snaptrade_activity_service),
):
    return await svc.delete_activity(id)