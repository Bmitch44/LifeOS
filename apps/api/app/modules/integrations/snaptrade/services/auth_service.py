from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.snaptrade_client import SnaptradeClient
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate

class SnaptradeAuthService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.snaptrade_connection_repo = SnaptradeConnectionRepo(session, clerk_user_id)
        self.snaptrade_client = SnaptradeClient(clerk_user_id)

    async def get_connection_portal(self) -> str:
        connection = await self.snaptrade_connection_repo.get_by_clerk_user_id()
        if not connection:
            new_snaptrade_user = self.snaptrade_client.register_user()
            payload = SnaptradeConnectionCreate(
                clerk_user_id=self.clerk_user_id,
                user_secret=new_snaptrade_user.get("user_secret"),
                connection_id=None,
                brokerage_name=None
            )
            connection = await self.snaptrade_connection_repo.create(payload)

        redirect_uri = self.snaptrade_client.create_connection_portal(connection.user_secret)
        return redirect_uri