from pydantic import BaseModel, Field
from typing import List
from app.modules.users.models import User


# class UserCreate(BaseModel):
#     email: str = Field(..., min_length=3)

class UserUpdate(BaseModel):
    email: str = Field(..., min_length=3)

class PaginatedUsers(BaseModel):
    items: List[User]
    page: int
    size: int
    total: int


