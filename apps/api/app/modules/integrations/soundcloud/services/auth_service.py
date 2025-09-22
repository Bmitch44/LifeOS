from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.soundcloud_api_client import SoundCloudClient
from app.modules.integrations.soundcloud.repos import TokenRepo
from app.modules.integrations.soundcloud.mappers.soundcloud_token_mapper import SoundcloudTokenMapper
from app.modules.integrations.soundcloud.schemas.token_schema import SoundcloudTokenCreate


class SoundcloudAuthService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.client = SoundCloudClient(clerk_user_id)
        self.token_repo = TokenRepo(session, clerk_user_id)
        self.token_mapper = SoundcloudTokenMapper(clerk_user_id)

    async def get_authorize_url(self) -> dict:
        url, verifier, state = self.client.build_authorize_url()
        # Caller should persist verifier+state (e.g. in temporary store tied to session)
        return {"authorize_url": url, "code_verifier": verifier, "state": state}

    async def exchange_code(self, code: str, code_verifier: str, state: str | None = None) -> dict:
        if not code or not code_verifier:
            raise HTTPException(status_code=400, detail="code and code_verifier are required")

        token = self.client.exchange_code_for_token(code=code, code_verifier=code_verifier)

        existing = await self.token_repo.get_by_clerk_user_id()
        payload: SoundcloudTokenCreate = self.token_mapper.map_api_token_to_soundcloud_token(token)
        if existing:
            saved = await self.token_repo.update(existing.id, payload)
        else:
            saved = await self.token_repo.create(payload)

        return {"token_id": saved.id}

    async def refresh(self) -> dict:
        existing = await self.token_repo.get_by_clerk_user_id()
        if not existing or not existing.refresh_token:
            raise HTTPException(status_code=400, detail="No refresh token available")
        token = self.client.refresh_access_token(refresh_token=existing.refresh_token)
        payload: SoundcloudTokenCreate = self.token_mapper.map_api_token_to_soundcloud_token(token)
        saved = await self.token_repo.update(existing.id, payload)
        return {"token_id": saved.id}


