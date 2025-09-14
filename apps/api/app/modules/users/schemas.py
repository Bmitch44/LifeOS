from pydantic import BaseModel, Field
from typing import List
from app.modules.users.models import User


class UserCreate(BaseModel):
    email: str = Field(..., min_length=3)
    client_id: str = Field(..., min_length=3)

class UserUpdate(UserCreate):
    pass

class PaginatedUsers(BaseModel):
    items: List[User]
    page: int
    size: int
    total: int


