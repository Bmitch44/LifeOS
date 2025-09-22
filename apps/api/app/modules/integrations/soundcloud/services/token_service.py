from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.soundcloud.repos import TokenRepo
from app.modules.integrations.soundcloud.schemas import SoundcloudTokenCreate, SoundcloudTokenUpdate
from app.db.models import SoundcloudToken
from app.clients.soundcloud_api_client import SoundCloudClient
from app.modules.integrations.soundcloud.mappers.soundcloud_token_mapper import SoundcloudTokenMapper


class TokenService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.repo = TokenRepo(session, clerk_user_id)
        self.mapper = SoundcloudTokenMapper(clerk_user_id)
        self.soundcloud_client = SoundCloudClient(clerk_user_id)

    async def create_token(self, payload: SoundcloudTokenCreate) -> SoundcloudToken:
        return await self.repo.create(payload)

    async def get_token(self, id: int) -> SoundcloudToken:
        return await self.repo.get(id)

    async def update_token(self, id: int, payload: SoundcloudTokenUpdate) -> SoundcloudToken:
        return await self.repo.update(id, payload)

    async def delete_token(self, id: int) -> dict:
        return await self.repo.delete(id)