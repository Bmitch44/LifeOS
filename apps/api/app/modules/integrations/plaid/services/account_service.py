from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.plaid.repos.account_repo import PlaidAccountRepo
from app.modules.integrations.plaid.schemas import PlaidAccountCreate, PlaidAccountUpdate, PaginatedPlaidAccounts
from app.modules.integrations.plaid.models import PlaidAccount, PlaidItem
from app.clients.plaid_client import PlaidClient

class PlaidAccountService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PlaidAccountRepo(session)
        self.plaid_client = PlaidClient()

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

    async def sync_accounts(self, clerk_user_id: str) -> dict:
        # Fetch all Plaid items to get their access tokens for the given clerk_user_id
        items_result = await self.session.execute(select(PlaidItem).where(PlaidItem.clerk_user_id == clerk_user_id))
        items = items_result.scalars().all()

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
                existing_result = await self.session.execute(
                    select(PlaidAccount).where(PlaidAccount.account_id == ext.account_id)
                )
                existing = existing_result.scalar_one_or_none()

                balances = getattr(ext, "balances", None)
                payload = PlaidAccountCreate(
                    clerk_user_id=item.clerk_user_id,
                    account_id=ext.account_id,
                    name=getattr(ext, "name", None),
                    official_name=getattr(ext, "official_name", None),
                    type=getattr(ext, "type", None),
                    subtype=getattr(ext, "subtype", None),
                    current_balance=getattr(balances, "current", None) if balances else None,
                    available_balance=getattr(balances, "available", None) if balances else None,
                    iso_currency_code=getattr(balances, "iso_currency_code", None) if balances else None,
                    mask=getattr(ext, "mask", None),
                )

                if existing:
                    await self.repo.update(existing.id, payload)
                else:
                    await self.repo.create(payload)

        return {"message": "Accounts synced successfully"}

