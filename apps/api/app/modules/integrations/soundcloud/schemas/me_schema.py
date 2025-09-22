from typing import Optional
from pydantic import BaseModel

class SoundcloudMeCreate(BaseModel):
    clerk_user_id: str
    urn: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    first_name: Optional[str] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    full_name: Optional[str] = None
    last_name: Optional[str] = None
    likes_count: Optional[int] = None
    permalink: Optional[str] = None
    permalink_url: Optional[str] = None
    plan: Optional[str] = None
    playlist_count: Optional[int] = None
    private_playlists_count: Optional[int] = None
    private_tracks_count: Optional[int] = None
    public_favorites_count: Optional[int] = None
    reposts_count: Optional[int] = None
    track_count: Optional[int] = None
    username: Optional[str] = None
    website: Optional[str] = None
    website_title: Optional[str] = None

class SoundcloudMeUpdate(SoundcloudMeCreate):
    pass