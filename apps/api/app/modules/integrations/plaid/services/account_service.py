from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.plaid.repos.account_repo import PlaidAccountRepo
from app.modules.integrations.plaid.schemas import PlaidAccountCreate, PlaidAccountUpdate, PaginatedPlaidAccounts
from app.modules.integrations.plaid.models import PlaidAccount
from app.clients.plaid_client import PlaidClient
from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from app.modules.integrations.plaid.mappers.plaid_account_to_finacial_account import PlaidAccountToFinancialAccountMapper

class PlaidAccountService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PlaidAccountRepo(session)
        self.mapper = PlaidAccountToFinancialAccountMapper()
        self.financial_account_repo = FinancialAccountRepo(session)
        self.item_repo = PlaidItemRepo(session)
        self.plaid_client = PlaidClient()

    async def list_accounts(self, clerk_user_id: str, page: int, size: int) -> PaginatedPlaidAccounts:
        return await self.repo.paginate(clerk_user_id, page, size)
        
    async def create_account(self, payload: PlaidAccountCreate) -> PlaidAccount:
        return await self.repo.create(payload)

    async def get_account(self, id: int) -> PlaidAccount:
        return await self.repo.get(id)

    async def update_account(self, id: int, payload: PlaidAccountUpdate) -> PlaidAccount:
        return await self.repo.update(id, payload)

    async def delete_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_accounts(self, clerk_user_id: str) -> dict:
        # Fetch all Plaid items to get their access tokens for the given clerk_user_id
        items = await self.item_repo.paginate(clerk_user_id, 1, 100)

        # If no items, return
        if not items:
            return {"message": "No items to sync"}

        # Sync each item
        for item in items:
            # One call per item: get all accounts from Plaid
            ext_accounts = await self.plaid_client.get_accounts(access_token=item.access_token)

            # Upsert by external account_id
            for ext in ext_accounts:
                # Find existing by Plaid account_id
                existing_account = await self.repo.get_by_account_id(ext.account_id)
                existing_financial_account = await self.financial_account_repo.get_by_source_account_id(ext.account_id)

                payload = self.mapper.map_api_account_to_plaid_account(clerk_user_id, ext)

                if existing_account:
                    updated_account = await self.repo.update(existing_account.id, payload)
                else:
                    updated_account = await self.repo.create(payload)

                if existing_financial_account:
                    await self.financial_account_repo.update(existing_financial_account.id, self.mapper.map_plaid_account_to_financial_account(updated_account))
                else:
                    await self.financial_account_repo.create(self.mapper.map_plaid_account_to_financial_account(updated_account))

        return {"message": "Accounts synced successfully"}

