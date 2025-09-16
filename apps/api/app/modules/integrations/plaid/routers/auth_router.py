from fastapi import APIRouter, Depends, Body

from app.modules.integrations.plaid.services import PlaidAuthService
from app.deps import get_current_user, get_plaid_auth_service
from app.core.auth import AuthenticatedUser
from app.db.models import PlaidItem

router = APIRouter(prefix="/v1/plaid/auth", tags=["plaid auth"])

@router.get("/link-token", response_model=str)
async def get_link_token(
    svc: PlaidAuthService = Depends(get_plaid_auth_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.get_link_token(auth_user.user_id)

@router.post("/exchange-public-token", response_model=PlaidItem)
async def exchange_public_token(
    public_token: str = Body(...),
    svc: PlaidAuthService = Depends(get_plaid_auth_service),
    auth_user: AuthenticatedUser = Depends(get_current_user),
):
    return await svc.exchange_public_token(auth_user.user_id, public_token)