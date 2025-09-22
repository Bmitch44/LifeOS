from fastapi import HTTPException
from app.modules.integrations.soundcloud.schemas import SoundcloudMeCreate, SoundcloudMeUpdate
from app.db.models import SoundcloudMe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select


class MeRepo:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id

    async def create(self, payload: SoundcloudMeCreate) -> SoundcloudMe:
        try:
            soundcloud_me = SoundcloudMe(
                clerk_user_id=payload.clerk_user_id,
                urn=payload.urn,
                avatar_url=payload.avatar_url,
                city=payload.city,
                country=payload.country,
                description=payload.description,
                first_name=payload.first_name,
                followers_count=payload.followers_count,
                following_count=payload.following_count,
                full_name=payload.full_name,
                last_name=payload.last_name,
                likes_count=payload.likes_count,
                permalink=payload.permalink,
                permalink_url=payload.permalink_url,
                plan=payload.plan,
                playlist_count=payload.playlist_count,
                private_playlists_count=payload.private_playlists_count,
                private_tracks_count=payload.private_tracks_count,
                public_favorites_count=payload.public_favorites_count,
                reposts_count=payload.reposts_count,
                track_count=payload.track_count,
                username=payload.username,
                website=payload.website,
                website_title=payload.website_title,
            )
            self.session.add(soundcloud_me)
            await self.session.commit()
            await self.session.refresh(soundcloud_me)
            return soundcloud_me
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> SoundcloudMe:
        try:
            soundcloud_me = await self.session.execute(
                select(SoundcloudMe).where(SoundcloudMe.id == id, SoundcloudMe.clerk_user_id == self.clerk_user_id)
            )
            if not soundcloud_me:
                raise HTTPException(status_code=404, detail="SoundcloudMe not found")
            return soundcloud_me.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_clerk_user_id(self) -> SoundcloudMe:
        try:
            soundcloud_me = await self.session.execute(select(SoundcloudMe).where(SoundcloudMe.clerk_user_id == self.clerk_user_id))
            if not soundcloud_me:
                raise HTTPException(status_code=404, detail="SoundcloudMe not found")
            return soundcloud_me.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SoundcloudMeUpdate) -> SoundcloudMe:
        try:
            soundcloud_me = await self.get(id)
            if not soundcloud_me:
                raise HTTPException(status_code=404, detail="SoundcloudMe not found")
            soundcloud_me.urn = payload.urn
            soundcloud_me.avatar_url = payload.avatar_url
            soundcloud_me.city = payload.city
            soundcloud_me.country = payload.country
            soundcloud_me.description = payload.description
            soundcloud_me.first_name = payload.first_name
            soundcloud_me.followers_count = payload.followers_count
            soundcloud_me.following_count = payload.following_count
            soundcloud_me.full_name = payload.full_name
            soundcloud_me.last_name = payload.last_name
            soundcloud_me.likes_count = payload.likes_count
            soundcloud_me.permalink = payload.permalink
            soundcloud_me.permalink_url = payload.permalink_url
            soundcloud_me.plan = payload.plan
            soundcloud_me.playlist_count = payload.playlist_count
            soundcloud_me.private_playlists_count = payload.private_playlists_count
            soundcloud_me.private_tracks_count = payload.private_tracks_count
            soundcloud_me.public_favorites_count = payload.public_favorites_count
            soundcloud_me.reposts_count = payload.reposts_count
            soundcloud_me.track_count = payload.track_count
            soundcloud_me.username = payload.username
            soundcloud_me.website = payload.website
            soundcloud_me.website_title = payload.website_title
            await self.session.commit()
            await self.session.refresh(soundcloud_me)
            return soundcloud_me
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            soundcloud_me = await self.get(id)
            if not soundcloud_me:
                raise HTTPException(status_code=404, detail="SoundcloudMe not found")
            await self.session.execute(delete(SoundcloudMe).where(SoundcloudMe.id == id))
            await self.session.commit()
            return {"message": "SoundcloudMe deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e


