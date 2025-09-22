from fastapi import HTTPException
from app.modules.integrations.soundcloud.schemas import SoundcloudTokenCreate, SoundcloudTokenUpdate
from app.db.models import SoundcloudToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select


class TokenRepo:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id

    async def create(self, payload: SoundcloudTokenCreate) -> SoundcloudToken:
        try:
            soundcloud_token = SoundcloudToken(
                clerk_user_id=payload.clerk_user_id,
                access_token=payload.access_token,
                token_type=payload.token_type,
                expires_in=payload.expires_in,
                refresh_token=payload.refresh_token,
                scope=payload.scope,
                expires_at=payload.expires_at,
            )
            self.session.add(soundcloud_token)
            await self.session.commit()
            await self.session.refresh(soundcloud_token)
            return soundcloud_token
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> SoundcloudToken:
        try:
            soundcloud_token = await self.session.execute(
                select(SoundcloudToken).where(SoundcloudToken.id == id, SoundcloudToken.clerk_user_id == self.clerk_user_id)
            )
            if not soundcloud_token:
                raise HTTPException(status_code=404, detail="SoundcloudToken not found")
            return soundcloud_token.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_clerk_user_id(self) -> SoundcloudToken:
        try:
            result = await self.session.execute(
                select(SoundcloudToken).where(SoundcloudToken.clerk_user_id == self.clerk_user_id)
            )
            token = result.scalar_one_or_none()
            if not token:
                return None  # type: ignore
            return token
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SoundcloudTokenUpdate) -> SoundcloudToken:
        try:
            soundcloud_token = await self.get(id)
            if not soundcloud_token:
                raise HTTPException(status_code=404, detail="SoundcloudToken not found")
            soundcloud_token.access_token = payload.access_token
            soundcloud_token.token_type = payload.token_type
            soundcloud_token.expires_in = payload.expires_in
            soundcloud_token.refresh_token = payload.refresh_token
            soundcloud_token.scope = payload.scope
            soundcloud_token.expires_at = payload.expires_at
            await self.session.commit()
            await self.session.refresh(soundcloud_token)
            return soundcloud_token
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            soundcloud_token = await self.get(id)
            if not soundcloud_token:
                raise HTTPException(status_code=404, detail="SoundcloudToken not found")
            await self.session.execute(delete(SoundcloudToken).where(SoundcloudToken.id == id))
            await self.session.commit()
            return {"message": "SoundcloudToken deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e


