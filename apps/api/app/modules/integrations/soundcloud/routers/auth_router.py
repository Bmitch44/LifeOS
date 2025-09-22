from fastapi import APIRouter, Depends, Body

from app.modules.integrations.soundcloud.services.auth_service import SoundcloudAuthService
from app.modules.integrations.soundcloud.deps import get_soundcloud_auth_service


router = APIRouter(prefix="/v1/soundcloud/auth", tags=["soundcloud auth"])


@router.get("/authorize", response_model=dict)
async def get_authorize(
    svc: SoundcloudAuthService = Depends(get_soundcloud_auth_service),
):
    return await svc.get_authorize_url()


@router.post("/exchange", response_model=dict)
async def exchange_code(
    code: str = Body(...),
    code_verifier: str = Body(...),
    state: str | None = Body(default=None),
    svc: SoundcloudAuthService = Depends(get_soundcloud_auth_service),
):
    return await svc.exchange_code(code=code, code_verifier=code_verifier, state=state)


@router.post("/refresh", response_model=dict)
async def refresh_token(
    svc: SoundcloudAuthService = Depends(get_soundcloud_auth_service),
):
    return await svc.refresh()


