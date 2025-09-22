from typing import Optional
from pydantic import BaseModel
from app.db.models import PlaidAccount

class PlaidAccountCreate(BaseModel):
    clerk_user_id: str
    plaid_account_id: str
    name: Optional[str]
    official_name: Optional[str]
    type: Optional[str]
    subtype: Optional[str]
    current_balance: Optional[float]
    available_balance: Optional[float]
    iso_currency_code: Optional[str]
    mask: Optional[str]

class PlaidAccountUpdate(PlaidAccountCreate):
    pass

class PaginatedPlaidAccounts(BaseModel):
    items: list[PlaidAccount]
    page: int
    size: int
    total: int