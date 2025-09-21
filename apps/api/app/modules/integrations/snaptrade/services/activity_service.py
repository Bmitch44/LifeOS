from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.repos.activity_repo import SnaptradeActivityRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeActivityCreate, SnaptradeActivityUpdate, PaginatedSnaptradeActivities
from app.modules.integrations.snaptrade.models import SnaptradeActivity
from app.clients.snaptrade_api_client import SnaptradeClient
from app.modules.integrations.snaptrade.mappers.snaptrade_activity_mapper import SnaptradeActivityMapper
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo


class SnaptradeActivityService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.repo = SnaptradeActivityRepo(session, clerk_user_id)
        self.mapper = SnaptradeActivityMapper(clerk_user_id)
        self.connection_repo = SnaptradeConnectionRepo(session, clerk_user_id)
        self.snaptrade_client = SnaptradeClient(clerk_user_id)

    async def list_activities(self, page: int, size: int) -> PaginatedSnaptradeActivities:
        return await self.repo.paginate(page, size)
        
    async def create_activity(self, payload: SnaptradeActivityCreate) -> SnaptradeActivity:
        return await self.repo.create(payload)

    async def get_activity(self, id: int) -> SnaptradeActivity:
        return await self.repo.get(id)

    async def update_activity(self, id: int, payload: SnaptradeActivityUpdate) -> SnaptradeActivity:
        return await self.repo.update(id, payload)

    async def delete_activity(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_activities(self, account_id: int) -> dict:
        connections_result = await self.connection_repo.paginate(1, 100)

        if connections_result.total == 0:
            return {"message": "No connections to sync"}

        for connection in connections_result.items:
            ext_activities = self.snaptrade_client.get_account_activities(connection.user_secret, account_id)

            for ext_activity in ext_activities:
                existing_activity = await self.repo.get_by_activity_id(ext_activity.get("id"))

                payload = self.mapper.map_api_account_to_snaptrade_account(ext_activity, account_id)

                if existing_activity:
                    await self.repo.update(existing_activity.id, payload)
                else:
                    await self.repo.create(payload)

        return {"message": "Activities synced successfully"}
        