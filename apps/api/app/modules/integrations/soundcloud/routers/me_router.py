from fastapi import APIRouter, Depends

from app.modules.integrations.soundcloud.schemas import SoundcloudMeCreate, SoundcloudMeUpdate
from app.modules.integrations.soundcloud.services import MeService
from app.modules.integrations.soundcloud.deps import get_soundcloud_me_service
from app.db.models import SoundcloudMe

router = APIRouter(prefix="/v1/soundcloud/me", tags=["soundcloud me"])

@router.post("", response_model=SoundcloudMe, status_code=201)
async def create_me(
    payload: SoundcloudMeCreate,
    svc: MeService = Depends(get_soundcloud_me_service),
):
    return await svc.create_me(payload)

@router.get("/sync", response_model=dict)
async def sync_me(
    svc: MeService = Depends(get_soundcloud_me_service),
):
    return await svc.sync_me()

@router.get("/{id}", response_model=SoundcloudMe)
async def get_me(
    id: int,
    svc: MeService = Depends(get_soundcloud_me_service),
):
    return await svc.get_me(id)

@router.put("/{id}", response_model=SoundcloudMe)
async def update_me(
    id: int,
    payload: SoundcloudMeUpdate,
    svc: MeService = Depends(get_soundcloud_me_service),
):
    return await svc.update_me(id, payload)

@router.delete("/{id}", response_model=dict)
async def delete_me(
    id: int,
    svc: MeService = Depends(get_soundcloud_me_service),
):
    return await svc.delete_me(id)