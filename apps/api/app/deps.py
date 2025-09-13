from typing import Annotated, Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repo import UsersRepo
from app.modules.users.service import UsersService
from app.core.auth import verify_bearer_token, AuthenticatedUser
from app.db.base import get_session

async def get_current_user(authorization: Optional[str] = Header(default=None)) -> AuthenticatedUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        return verify_bearer_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_users_service(repo: Annotated[UsersRepo, Depends(lambda: UsersRepo())]) -> UsersService:
    return UsersService(repo)

DbSession = Annotated[AsyncSession, Depends(get_session)]


