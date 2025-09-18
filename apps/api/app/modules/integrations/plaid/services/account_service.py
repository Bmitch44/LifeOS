from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.plaid.repos.account_repo import PlaidAccountRepo
from app.modules.integrations.plaid.schemas import PlaidAccountCreate, PlaidAccountUpdate, PaginatedPlaidAccounts
from app.modules.integrations.plaid.models import PlaidAccount
from app.clients.plaid_client import PlaidClient
from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from app.modules.integrations.plaid.mappers.plaid_account_mapper import PlaidAccountToFinancialAccountMapper

class PlaidAccountService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.repo = PlaidAccountRepo(session, clerk_user_id)
        self.financial_account_repo = FinancialAccountRepo(session, clerk_user_id)
        self.item_repo = PlaidItemRepo(session, clerk_user_id)
        self.mapper = PlaidAccountToFinancialAccountMapper(clerk_user_id)
        self.plaid_client = PlaidClient(clerk_user_id)

    async def list_accounts(self, page: int, size: int) -> PaginatedPlaidAccounts:
        return await self.repo.paginate(page, size)
        
    async def create_account(self, payload: PlaidAccountCreate) -> PlaidAccount:
        return await self.repo.create(payload)

    async def get_account(self, id: int) -> PlaidAccount:
        return await self.repo.get(id)

    async def update_account(self, id: int, payload: PlaidAccountUpdate) -> PlaidAccount:
        return await self.repo.update(id, payload)

    async def delete_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_accounts(self) -> dict:
        items_result = await self.item_repo.paginate(1, 100)

        if items_result.total == 0:
            return {"message": "No items to sync"}

        for item in items_result.items:
            ext_accounts = await self.plaid_client.get_accounts(access_token=item.access_token)

            for ext in ext_accounts:
                existing_account = await self.repo.get_by_account_id(ext.account_id)
                existing_financial_account = await self.financial_account_repo.get_by_source_account_id(ext.account_id)

                payload = self.mapper.map_api_account_to_plaid_account(ext)

                if existing_account:
                    updated_account = await self.repo.update(existing_account.id, payload)
                else:
                    updated_account = await self.repo.create(payload)

                if existing_financial_account:
                    await self.financial_account_repo.update(existing_financial_account.id, self.mapper.map_plaid_account_to_financial_account(updated_account))
                else:
                    await self.financial_account_repo.create(self.mapper.map_plaid_account_to_financial_account(updated_account))

        return {"message": "Accounts synced successfully"}

