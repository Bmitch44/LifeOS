from fastapi import APIRouter, Depends

from app.core.auth import AuthenticatedUser
from app.deps import get_current_user, get_snaptrade_auth_service
from app.modules.integrations.snaptrade.services.auth_service import SnaptradeAuthService

router = APIRouter(prefix="/v1/snaptrade/auth", tags=["snaptrade auth"])

@router.post("/connection-portal", response_model=str)
async def create_connection_portal(
    svc: SnaptradeAuthService = Depends(get_snaptrade_auth_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.create_connection_portal(auth_user.user_id)