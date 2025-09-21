from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_session, get_current_user
from app.core.auth import AuthenticatedUser


def get_snaptrade_connection_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.snaptrade.services import SnaptradeConnectionService
    return SnaptradeConnectionService(session, auth_user.user_id)

def get_snaptrade_account_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.snaptrade.services import SnaptradeAccountService
    return SnaptradeAccountService(session, auth_user.user_id)

def get_snaptrade_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.snaptrade.services import SnaptradeAuthService
    return SnaptradeAuthService(session, auth_user.user_id)

def get_snaptrade_activity_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.snaptrade.services import SnaptradeActivityService
    return SnaptradeActivityService(session, auth_user.user_id)