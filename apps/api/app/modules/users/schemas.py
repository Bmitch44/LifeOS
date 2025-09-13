from pydantic import BaseModel, Field
from typing import List


class UserOut(BaseModel):
    id: int
    email: str


class UserCreate(BaseModel):
    email: str = Field(..., min_length=3)


class PaginatedUsers(BaseModel):
    items: List[UserOut]
    page: int
    size: int
    total: int


