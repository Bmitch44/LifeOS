from fastapi import Depends
from app.deps import get_session, get_current_user
from app.core.auth import AuthenticatedUser

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession


def get_plaid_item_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    ):
    from app.modules.integrations.plaid.services import PlaidItemService
    return PlaidItemService(session, auth_user.user_id)

def get_plaid_account_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.plaid.services import PlaidAccountService
    return PlaidAccountService(session, auth_user.user_id)

def get_plaid_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.plaid.services import PlaidAuthService
    return PlaidAuthService(session, auth_user.user_id)