from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import AuthenticatedUser
from app.deps import get_current_user
from app.db.base import get_session
from app.modules.finances.services import FinancialAccountService


def get_financial_account_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
):
    return FinancialAccountService(session, auth_user.user_id)
