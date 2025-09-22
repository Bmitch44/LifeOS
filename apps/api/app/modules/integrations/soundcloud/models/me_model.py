from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SoundcloudMe(SQLModel, table=True):
    __tablename__ = "soundcloud_me"
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    urn: str = Field(nullable=True)
    avatar_url: str = Field(nullable=True)
    city: str = Field(nullable=True)
    country: str = Field(nullable=True)
    description: str = Field(nullable=True)
    first_name: str = Field(nullable=True)
    followers_count: int = Field(nullable=True)
    following_count: int = Field(nullable=True)
    full_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    likes_count: int = Field(nullable=True)
    permalink: str = Field(nullable=True)
    permalink_url: str = Field(nullable=True)
    plan: str = Field(nullable=True)
    playlist_count: int = Field(nullable=True)
    private_playlists_count: int = Field(nullable=True)
    public_favorites_count: int = Field(nullable=True)
    track_count: int = Field(nullable=True)
    private_tracks_count: int = Field(nullable=True)
    reposts_count: int = Field(nullable=True)
    username: str = Field(nullable=True)
    website: str = Field(nullable=True)
    website_title: str = Field(nullable=True)
    created_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now())
    updated_at: datetime = Field(nullable=True, default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})