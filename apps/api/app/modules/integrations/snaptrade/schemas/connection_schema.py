from pydantic import BaseModel
from typing import Optional
class SnaptradeConnectionCreate(BaseModel):
    clerk_user_id: str
    connection_id: Optional[str] = None
    user_secret: Optional[str] = None
    brokerage_name: Optional[str] = None

class SnaptradeConnectionUpdate(SnaptradeConnectionCreate):
    pass