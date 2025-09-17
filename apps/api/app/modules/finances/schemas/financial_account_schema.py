from pydantic import BaseModel
from typing import List, Optional
from app.db.models import FinancialAccount


class FinancialAccountCreate(BaseModel):
    clerk_user_id: str
    type: Optional[str] = None
    name: Optional[str] = None
    institution_name: Optional[str] = None
    currency: Optional[str] = None
    current_balance: Optional[float] = None
    source: str
    source_account_id: str


class FinancialAccountUpdate(FinancialAccountCreate):
    pass


class PaginatedFinancialAccounts(BaseModel):
    items: List[FinancialAccount]
    page: int
    size: int
    total: int


