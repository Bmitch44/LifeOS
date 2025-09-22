from typing import Dict
from app.modules.integrations.soundcloud.schemas.token_schema import SoundcloudTokenCreate
from app.core.exceptions import MapperError     

class SoundcloudTokenMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_api_token_to_soundcloud_token(self, api_token: Dict) -> SoundcloudTokenCreate:
        try:
            return SoundcloudTokenCreate(
                clerk_user_id=self.clerk_user_id,
                access_token=api_token.get("access_token"),
                token_type=api_token.get("token_type"),
                expires_in=api_token.get("expires_in"),
                refresh_token=api_token.get("refresh_token"),
                scope=api_token.get("scope"),
                expires_at=api_token.get("expires_at"),
            )
        except Exception as e:
            raise MapperError(source="api token", target="soundcloud token", e=e) from e