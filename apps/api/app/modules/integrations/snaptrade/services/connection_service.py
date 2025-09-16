from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate, SnaptradeConnectionUpdate
from app.modules.integrations.snaptrade.models import SnaptradeConnection
from app.clients.snaptrade_client import SnaptradeClient


class SnaptradeConnectionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SnaptradeConnectionRepo(session)
        self.snaptrade_client = SnaptradeClient()

    async def create_connection(self, payload: SnaptradeConnectionCreate) -> SnaptradeConnection:
        return await self.repo.create(payload)

    async def get_connection(self, id: int) -> SnaptradeConnection:
        return await self.repo.get(id)

    async def update_connection(self, id: int, payload: SnaptradeConnectionUpdate) -> SnaptradeConnection:
        return await self.repo.update(id, payload)

    async def delete_connection(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_connections(self, clerk_user_id: str) -> dict:
        # Fetch all Snaptrade connections to get their connection_ids for the given clerk_user_id
        connections_result = await self.session.execute(select(SnaptradeConnection).where(SnaptradeConnection.clerk_user_id == clerk_user_id))
        connections = connections_result.scalars().all()

        # If no connections, return
        if not connections:
            return {"message": "No connections to sync"}

        ext_connections = await self.snaptrade_client.get_connections(clerk_user_id)

        # Upsert by external connection_id
        for ext in ext_connections:
            # Find existing by Snaptrade connection_id
            existing_result = await self.session.execute(
                select(SnaptradeConnection).where(SnaptradeConnection.connection_id == ext.get("connection_id"))
            )
            existing = existing_result.scalar_one_or_none()

            payload = SnaptradeConnectionCreate(
                clerk_user_id=clerk_user_id,
                connection_id=ext.get("connection_id"),
                brokerage_name=ext.get("brokerage_name")
            )

            if existing:
                await self.repo.update(existing.id, payload)
            else:
                await self.repo.create(payload)

        return {"message": "Connections synced successfully"}