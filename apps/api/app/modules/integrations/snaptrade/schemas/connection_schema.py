from typing_extensions import List
from pydantic import BaseModel
from typing import Optional
from app.db.models import SnaptradeConnection

class SnaptradeConnectionCreate(BaseModel):
    clerk_user_id: str
    connection_id: Optional[str] = None
    user_secret: Optional[str] = None
    brokerage_name: Optional[str] = None

class SnaptradeConnectionUpdate(SnaptradeConnectionCreate):
    pass


class PaginatedSnaptradeConnections(BaseModel):
    items: List[SnaptradeConnection]
    page: int
    size: int
    total: int