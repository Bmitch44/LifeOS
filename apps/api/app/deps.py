from typing import Annotated, Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.auth import verify_bearer_token, AuthenticatedUser
from app.db.base import get_session
from app.db.models import User

async def get_current_user(
    authorization: Optional[str] = Header(default=None),
    session: Annotated[AsyncSession, Depends(get_session)] = None,
) -> AuthenticatedUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        auth_user = verify_bearer_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, message=str(f"Invalid token: {e}"))

    # Ensure 1:1 mapping in DB by Clerk user id (token.sub -> User.client_id)
    try:
        result = await session.execute(select(User).where(User.clerk_user_id == auth_user.user_id))
        user = result.scalar_one_or_none()
        if user is None:
            session.add(
                User(
                    clerk_user_id=auth_user.user_id, 
                    email=auth_user.email, 
                    first_name=auth_user.first_name, 
                    last_name=auth_user.last_name, 
                    phone=auth_user.phone
                )
            )
            await session.commit()
        elif auth_user.email and user.email != auth_user.email:
            user.email = auth_user.email
            await session.commit()
    except IntegrityError:
        await session.rollback()
        # Another request may have created it concurrently; ignore
    except Exception:
        await session.rollback()
        # Do not block auth on DB errors

    return auth_user


def get_users_service(session: Annotated[AsyncSession, Depends(get_session)]):
    from app.modules.users.service import UsersService
    return UsersService(session)

def get_courses_service(session: Annotated[AsyncSession, Depends(get_session)]):
    from app.modules.school.courses.service import CoursesService
    return CoursesService(session)

def get_assesments_service(session: Annotated[AsyncSession, Depends(get_session)]):
    from app.modules.school.assesments.service import AssesmentsService
    return AssesmentsService(session)