from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_session, get_current_user
from app.core.auth import AuthenticatedUser


def get_soundcloud_auth_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.soundcloud.services import SoundcloudAuthService
    return SoundcloudAuthService(session, auth_user.user_id)

def get_soundcloud_me_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.soundcloud.services import MeService
    return MeService(session, auth_user.user_id)

def get_soundcloud_token_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    from app.modules.integrations.soundcloud.services import TokenService
    return TokenService(session, auth_user.user_id)

