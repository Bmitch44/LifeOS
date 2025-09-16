from pydantic import BaseModel
from app.db.models import PlaidAccount

class PlaidAccountCreate(BaseModel):
    clerk_user_id: str
    account_id: str
    name: str
    official_name: str
    type: str
    subtype: str
    current_balance: float
    available_balance: float
    iso_currency_code: str
    mask: str

class PlaidAccountUpdate(PlaidAccountCreate):
    pass

class PaginatedPlaidAccounts(BaseModel):
    items: list[PlaidAccount]
    page: int
    size: int
    total: int