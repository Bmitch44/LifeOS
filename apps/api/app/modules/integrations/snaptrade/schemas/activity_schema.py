from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.modules.integrations.snaptrade.models import SnaptradeActivity

class SnaptradeActivityCreate(BaseModel):
    clerk_user_id: str
    activity_id: str
    account_id: int
    symbol_id: Optional[str]
    option_symbol_id: Optional[str]
    type: Optional[str]
    option_type: Optional[str]
    price: Optional[float] = None
    units: Optional[float] = None
    amount: Optional[float]
    description: Optional[str] = None
    trade_date: Optional[datetime]
    settlement_date: Optional[datetime] = None
    currency: str
    fees: Optional[float] = None
    fx_rate: Optional[float]
    institution: Optional[str] = None

class SnaptradeActivityUpdate(SnaptradeActivityCreate):
    pass

class PaginatedSnaptradeActivities(BaseModel):
    items: List[SnaptradeActivity]
    page: int
    size: int
    total: int