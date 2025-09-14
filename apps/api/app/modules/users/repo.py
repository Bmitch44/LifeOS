from fastapi import HTTPException
from app.modules.users.schemas import UserCreate, PaginatedUsers, UserUpdate
from app.modules.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete


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
            
            return PaginatedUsers(items=users, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: UserCreate) -> User:
        try:
            user = User(email=payload.email, client_id=payload.client_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> User:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: UserUpdate) -> User:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.email = payload.email
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            user = await self.session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await self.session.execute(delete(User).where(User.id == id))
            await self.session.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e


