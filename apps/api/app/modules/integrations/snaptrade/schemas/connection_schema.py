from pydantic import BaseModel

class SnaptradeConnectionCreate(BaseModel):
    clerk_user_id: str
    connection_id: str
    user_secret: str = None
    brokerage_name: str = None

class SnaptradeConnectionUpdate(SnaptradeConnectionCreate):
    pass