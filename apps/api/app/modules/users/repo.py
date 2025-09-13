from app.modules.users.schemas import UserCreate, PaginatedUsers, UserOut


class UsersRepo:
    async def paginate(self, page: int, size: int) -> PaginatedUsers:
        # Placeholder in-memory data
        start = (page - 1) * size
        end = start + size
        data = [UserOut(id=i + 1, email=f"user{i+1}@example.com") for i in range(50)]
        return PaginatedUsers(items=data[start:end], page=page, size=size, total=len(data))

    async def insert(self, payload: UserCreate) -> UserOut:
        return UserOut(id=1, email=payload.email)


