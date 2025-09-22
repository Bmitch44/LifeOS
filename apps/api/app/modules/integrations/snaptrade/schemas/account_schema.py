from typing import List, Optional
from pydantic import BaseModel
from app.db.models import SnaptradeAccount

class SnaptradeAccountCreate(BaseModel):
    clerk_user_id: str
    snaptrade_account_id: str
    connection_id: int
    name: Optional[str]
    number: Optional[str]
    institution_name: Optional[str]
    status: Optional[str]
    type: Optional[str]
    current_balance: Optional[float]
    currency: Optional[str]

class SnaptradeAccountUpdate(SnaptradeAccountCreate):
    pass

class PaginatedSnaptradeAccounts(BaseModel):
    items: List[SnaptradeAccount]
    page: int
    size: int
    total: int