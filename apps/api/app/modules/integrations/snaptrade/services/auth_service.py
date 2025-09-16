from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.snaptrade_client import SnaptradeClient
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate

class SnaptradeAuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.snaptrade_connection_repo = SnaptradeConnectionRepo(session)
        self.snaptrade_client = SnaptradeClient()

    async def create_connection_portal(self, clerk_user_id: str) -> str:
        connection = await self.snaptrade_connection_repo.get_by_clerk_user_id(clerk_user_id)
        if not connection:
            new_snaptrade_user = await self.snaptrade_client.register_user(clerk_user_id)
            payload = SnaptradeConnectionCreate(
                clerk_user_id=clerk_user_id,
                connection_id=new_snaptrade_user.get("user_id"),
                user_secret=new_snaptrade_user.get("user_secret"),
                brokerage_name=None
            )
            connection = await self.snaptrade_connection_repo.create(payload)

        redirect_uri = await self.snaptrade_client.create_connection_portal(clerk_user_id, connection.user_secret)
        return redirect_uri