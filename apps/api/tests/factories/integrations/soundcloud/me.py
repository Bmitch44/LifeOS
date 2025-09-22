from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SoundcloudMe


async def create_soundcloud_me(
    session: AsyncSession,
    *,
    clerk_user_id: str = "test_user",
    urn: Optional[str] = "soundcloud:users:1",
    avatar_url: Optional[str] = "http://avatar",
    city: Optional[str] = "City",
    country: Optional[str] = "Country",
    description: Optional[str] = "Desc",
    first_name: Optional[str] = "First",
    followers_count: Optional[int] = 1,
    following_count: Optional[int] = 2,
    full_name: Optional[str] = "Full Name",
    last_name: Optional[str] = "Last",
    likes_count: Optional[int] = 3,
    permalink: Optional[str] = "me",
    permalink_url: Optional[str] = "http://sc/me",
    plan: Optional[str] = "free",
    playlist_count: Optional[int] = 0,
    private_playlists_count: Optional[int] = 0,
    private_tracks_count: Optional[int] = 0,
    public_favorites_count: Optional[int] = 0,
    reposts_count: Optional[int] = 0,
    track_count: Optional[int] = 0,
    username: Optional[str] = "user",
    website: Optional[str] = "http://site",
    website_title: Optional[str] = "site",
) -> SoundcloudMe:
    obj = SoundcloudMe(
        clerk_user_id=clerk_user_id,
        urn=urn,
        avatar_url=avatar_url,
        city=city,
        country=country,
        description=description,
        first_name=first_name,
        followers_count=followers_count,
        following_count=following_count,
        full_name=full_name,
        last_name=last_name,
        likes_count=likes_count,
        permalink=permalink,
        permalink_url=permalink_url,
        plan=plan,
        playlist_count=playlist_count,
        private_playlists_count=private_playlists_count,
        private_tracks_count=private_tracks_count,
        public_favorites_count=public_favorites_count,
        reposts_count=reposts_count,
        track_count=track_count,
        username=username,
        website=website,
        website_title=website_title,
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


