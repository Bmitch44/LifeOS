from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate, SnaptradeConnectionUpdate, PaginatedSnaptradeConnections
from app.modules.integrations.snaptrade.models import SnaptradeConnection
from app.clients.snaptrade_client import SnaptradeClient
from app.modules.integrations.snaptrade.mappers.snaptrade_connection_mapper import SnaptradeConnectionMapper


class SnaptradeConnectionService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.repo = SnaptradeConnectionRepo(session, clerk_user_id)
        self.mapper = SnaptradeConnectionMapper(clerk_user_id)
        self.snaptrade_client = SnaptradeClient(clerk_user_id)

    async def list_connections(self, page: int, size: int) -> PaginatedSnaptradeConnections:
        return await self.repo.paginate(page, size)

    async def create_connection(self, payload: SnaptradeConnectionCreate) -> SnaptradeConnection:
        return await self.repo.create(payload)

    async def get_connection(self, id: int) -> SnaptradeConnection:
        return await self.repo.get(id)

    async def update_connection(self, id: int, payload: SnaptradeConnectionUpdate) -> SnaptradeConnection:
        return await self.repo.update(id, payload)

    async def delete_connection(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_connections(self) -> dict:
        # Fetch all Snaptrade connections to get their connection_ids for the given clerk_user_id
        connections_result = await self.repo.paginate(1, 100)

        # If no connections, return
        if connections_result.total == 0:
            return {"message": "No connections to sync"}

        for connection in connections_result.items:

            ext_connections = self.snaptrade_client.get_connections(connection.user_secret)

            # Upsert by external connection_id
            for ext in ext_connections:
                # Find existing by Snaptrade connection_id
                existing = await self.repo.get_by_connection_id(ext.get("id"))

                payload = self.mapper.map_api_connection_to_snaptrade_connection(ext, connection.user_secret)

                if existing:
                    await self.repo.update(existing.id, payload)
                else:
                    await self.repo.create(payload)

        return {"message": "Connections synced successfully"}