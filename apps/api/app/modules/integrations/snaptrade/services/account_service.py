from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.repos.account_repo import SnaptradeAccountRepo
from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate
from app.modules.integrations.snaptrade.models import SnaptradeAccount
from app.clients.snaptrade_client import SnaptradeClient


class SnaptradeAccountService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SnaptradeAccountRepo(session)
        self.snaptrade_client = SnaptradeClient()
        
    async def create_account(self, payload: SnaptradeAccountCreate) -> SnaptradeAccount:
        return await self.repo.create(payload)

    async def get_account(self, id: int) -> SnaptradeAccount:
        return await self.repo.get(id)

    async def update_account(self, id: int, payload: SnaptradeAccountUpdate) -> SnaptradeAccount:
        return await self.repo.update(id, payload)

    async def delete_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_accounts(self, clerk_user_id: str) -> dict:
        # Fetch all Snaptrade accounts to get their account_ids for the given clerk_user_id
        accounts_result = await self.session.execute(select(SnaptradeAccount).where(SnaptradeAccount.clerk_user_id == clerk_user_id))
        accounts = accounts_result.scalars().all()

        # If no accounts, return
        if not accounts:
            return {"message": "No accounts to sync"}

        ext_accounts = await self.snaptrade_client.get_accounts(clerk_user_id)

        # Upsert by external account_id
        for ext in ext_accounts:
            # Find existing by Snaptrade account_id
            existing_result = await self.session.execute(
                select(SnaptradeAccount).where(SnaptradeAccount.account_id == ext.get("account_id"))
            )
            existing = existing_result.scalar_one_or_none()

            payload = SnaptradeAccountCreate(
                clerk_user_id=clerk_user_id,
                account_id=ext.get("account_id"),
                connection_id=ext.get("connection_id"),
                name=ext.get("name"),
                number=ext.get("number"),
                institution_name=ext.get("institution_name"),
                status=ext.get("status"),
                type=ext.get("type"),
                current_balance=ext.get("current_balance"),
                currency=ext.get("currency")
            )

            if existing:
                await self.repo.update(existing.id, payload)
            else:
                await self.repo.create(payload)

        return {"message": "Accounts synced successfully"}
        