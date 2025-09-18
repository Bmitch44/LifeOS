from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.repos.account_repo import SnaptradeAccountRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate, PaginatedSnaptradeAccounts
from app.modules.integrations.snaptrade.models import SnaptradeAccount
from app.clients.snaptrade_api_client import SnaptradeClient
from app.modules.integrations.snaptrade.mappers.snaptrade_account_mapper import SnaptradeAccountMapper
from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo


class SnaptradeAccountService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.repo = SnaptradeAccountRepo(session, clerk_user_id)
        self.mapper = SnaptradeAccountMapper(clerk_user_id)
        self.connection_repo = SnaptradeConnectionRepo(session, clerk_user_id)
        self.financial_account_repo = FinancialAccountRepo(session, clerk_user_id)
        self.snaptrade_client = SnaptradeClient(clerk_user_id)

    async def list_accounts(self, page: int, size: int) -> PaginatedSnaptradeAccounts:
        return await self.repo.paginate(page, size)
        
    async def create_account(self, payload: SnaptradeAccountCreate) -> SnaptradeAccount:
        return await self.repo.create(payload)

    async def get_account(self, id: int) -> SnaptradeAccount:
        return await self.repo.get(id)

    async def update_account(self, id: int, payload: SnaptradeAccountUpdate) -> SnaptradeAccount:
        return await self.repo.update(id, payload)

    async def delete_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_accounts(self) -> dict:
        connections_result = await self.connection_repo.paginate(1, 100)

        if connections_result.total == 0:
            return {"message": "No connections to sync"}

        for connection in connections_result.items:
            ext_accounts = self.snaptrade_client.get_accounts(connection.user_secret)

            for ext_account in ext_accounts:
                existing_account = await self.repo.get_by_account_id(ext_account.get("id"))
                existing_financial_account = await self.financial_account_repo.get_by_source_account_id(ext_account.get("id"))

                payload = self.mapper.map_api_account_to_snaptrade_account(ext_account)

                if existing_account:
                    updated_account = await self.repo.update(existing_account.id, payload)
                else:
                    updated_account = await self.repo.create(payload)

                if existing_financial_account:
                    await self.financial_account_repo.update(existing_financial_account.id, self.mapper.map_snaptrade_account_to_financial_account(updated_account))
                else:
                    await self.financial_account_repo.create(self.mapper.map_snaptrade_account_to_financial_account(updated_account))


        return {"message": "Accounts synced successfully"}
        