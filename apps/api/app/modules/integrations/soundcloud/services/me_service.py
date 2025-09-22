from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.soundcloud.repos import MeRepo
from app.modules.integrations.soundcloud.schemas import SoundcloudMeCreate, SoundcloudMeUpdate
from app.db.models import SoundcloudMe
from app.clients.soundcloud_api_client import SoundCloudClient
from app.modules.integrations.soundcloud.mappers.soundcloud_me_mapper import SoundcloudMeMapper
from app.modules.integrations.soundcloud.repos import TokenRepo


class MeService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.repo = MeRepo(session, clerk_user_id)
        self.mapper = SoundcloudMeMapper(clerk_user_id)
        self.token_repo = TokenRepo(session, clerk_user_id)
        self.soundcloud_client = SoundCloudClient(clerk_user_id)

    async def create_me(self, payload: SoundcloudMeCreate) -> SoundcloudMe:
        return await self.repo.create(payload)

    async def get_me(self, id: int) -> SoundcloudMe:
        return await self.repo.get(id)

    async def update_me(self, id: int, payload: SoundcloudMeUpdate) -> SoundcloudMe:
        return await self.repo.update(id, payload)

    async def delete_me(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_me(self) -> dict:
        token = await self.token_repo.get_by_clerk_user_id()
        ext_me = self.soundcloud_client.get_me(token=token)
        existing_me = await self.repo.get_by_clerk_user_id()
        payload = self.mapper.map_api_me_to_soundcloud_me(ext_me)
        if existing_me:
            return await self.repo.update(existing_me.id, payload)
        else:
            return await self.repo.create(payload)