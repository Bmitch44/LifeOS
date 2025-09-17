from typing import List
from pydantic import BaseModel
from app.db.models import SnaptradeAccount

class SnaptradeAccountCreate(BaseModel):
    clerk_user_id: str
    account_id: str
    connection_id: str
    name: str
    number: str
    institution_name: str
    status: str
    type: str
    current_balance: float
    currency: str

class SnaptradeAccountUpdate(SnaptradeAccountCreate):
    pass

class PaginatedSnaptradeAccounts(BaseModel):
    items: List[SnaptradeAccount]
    page: int
    size: int
    total: int