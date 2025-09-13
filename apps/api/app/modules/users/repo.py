from fastapi import HTTPException
from app.modules.users.schemas import UserCreate, PaginatedUsers, UserOut, UserUpdate
from app.modules.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class UsersRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedUsers:
        try:
            # Calculate offset for pagination
            offset = (page - 1) * size
            
            # Get total count for pagination metadata (SQLAlchemy 2.x)
            total_query = select(func.count()).select_from(User)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            
            # Fetch only the users for the current page
            users_query = select(User).offset(offset).limit(size)
            users_result = await self.session.execute(users_query)
            users = users_result.scalars().all()
            users = [UserOut(id=user.id, email=user.email) for user in users]
            
            return PaginatedUsers(items=users, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: UserCreate) -> UserOut:
        try:
            user = User(email=payload.email)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return UserOut(id=user.id, email=user.email)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> UserOut:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserOut(id=id, email=user.email)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: UserUpdate) -> UserOut:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.email = payload.email
            await self.session.commit()
            await self.session.refresh(user)
            return UserOut(id=id, email=user.email)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> UserOut:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await self.session.delete(user)
            await self.session.commit()
            await self.session.refresh(user)
            return UserOut(id=id, email=user.email)
        except Exception as e:
            await self.session.rollback()
            raise e


