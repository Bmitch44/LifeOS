from typing import Dict
from app.modules.integrations.soundcloud.schemas.me_schema import SoundcloudMeCreate
from app.core.exceptions import MapperError


class SoundcloudMeMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_api_me_to_soundcloud_me(self, api_me: Dict) -> SoundcloudMeCreate:
        try:
            return SoundcloudMeCreate(
                clerk_user_id=self.clerk_user_id,
                urn=api_me.get("urn"),
                avatar_url=api_me.get("avatar_url"),
                city=api_me.get("city"),
                country=api_me.get("country"),
                description=api_me.get("description"),
                first_name=api_me.get("first_name"),
                followers_count=api_me.get("followers_count"),
                following_count=api_me.get("following_count"),
                full_name=api_me.get("full_name"),
                last_name=api_me.get("last_name"),
                likes_count=api_me.get("likes_count"),
                permalink=api_me.get("permalink"),
                permalink_url=api_me.get("permalink_url"),
                plan=api_me.get("plan"),
                playlist_count=api_me.get("playlist_count"),
                private_playlists_count=api_me.get("private_playlists_count"),
                private_tracks_count=api_me.get("private_tracks_count"),
                public_favorites_count=api_me.get("public_favorites_count"),
                reposts_count=api_me.get("reposts_count"),
                track_count=api_me.get("track_count"),
                username=api_me.get("username"),
                website=api_me.get("website"),
                website_title=api_me.get("website_title"),
            )
        except Exception as e:
            raise MapperError(source="api me", target="soundcloud me", e=e) from e