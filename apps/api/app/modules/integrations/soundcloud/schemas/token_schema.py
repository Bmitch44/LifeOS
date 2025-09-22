from datetime import datetime
from pydantic import BaseModel

class SoundcloudTokenCreate(BaseModel):
    clerk_user_id: str
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    expires_at: datetime

class SoundcloudTokenUpdate(SoundcloudTokenCreate):
    pass