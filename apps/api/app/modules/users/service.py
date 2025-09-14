from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repo import UsersRepo
from app.modules.users.schemas import PaginatedUsers, UserUpdate
from app.modules.users.models import User


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UsersRepo(session)

    async def list_users(self, page: int, size: int) -> PaginatedUsers:
        return await self.repo.paginate(page, size)

    async def get_user(self, id: int) -> User:
        return await self.repo.get(id)

    async def update_user(self, id: int, payload: UserUpdate) -> User:
        return await self.repo.update(id, payload)

    async def delete_user(self, id: int) -> dict:
        return await self.repo.delete(id)


