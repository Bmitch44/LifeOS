from .repo import UsersRepo
from .schemas import UserCreate, PaginatedUsers, UserOut


class UsersService:
    def __init__(self, repo: UsersRepo):
        self.repo = repo

    async def list_users(self, page: int, size: int) -> PaginatedUsers:
        return await self.repo.paginate(page, size)

    async def create_user(self, payload: UserCreate) -> UserOut:
        return await self.repo.insert(payload)


