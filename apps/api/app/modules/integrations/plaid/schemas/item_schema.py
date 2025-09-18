from pydantic import BaseModel
from app.db.models import PlaidItem
from typing import Optional

class PlaidItemCreate(BaseModel):
    clerk_user_id: str
    item_id: str
    access_token: str
    institution_name: Optional[str] = None

class PlaidItemUpdate(PlaidItemCreate):
    access_token: Optional[str] = None

class PaginatedPlaidItems(BaseModel):
    items: list[PlaidItem]
    page: int
    size: int
    total: int