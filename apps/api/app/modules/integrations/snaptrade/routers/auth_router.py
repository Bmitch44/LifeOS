from fastapi import APIRouter, Depends

from app.modules.integrations.snaptrade.deps import get_snaptrade_auth_service
from app.modules.integrations.snaptrade.services.auth_service import SnaptradeAuthService

router = APIRouter(prefix="/v1/snaptrade/auth", tags=["snaptrade auth"])

@router.get("/connection-portal", response_model=str)
async def get_connection_portal(
    svc: SnaptradeAuthService = Depends(get_snaptrade_auth_service),
):
    return await svc.get_connection_portal()