from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from app.modules.finances.schemas import FinancialAccountCreate, FinancialAccountUpdate, PaginatedFinancialAccounts
from app.modules.finances.models import FinancialAccount
from app.modules.integrations.plaid.services import PlaidAccountService
from app.modules.integrations.snaptrade.services import SnaptradeAccountService


class FinancialAccountService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = FinancialAccountRepo(session)
        self.plaid_account_service = PlaidAccountService(session)
        self.snaptrade_account_service = SnaptradeAccountService(session)

    async def list_financial_accounts(self, clerk_user_id: str, page: int, size: int) -> PaginatedFinancialAccounts:
        return await self.repo.paginate(clerk_user_id, page, size)
        
    async def create_financial_account(self, payload: FinancialAccountCreate) -> FinancialAccount:
        return await self.repo.create(payload)

    async def get_financial_account(self, id: int) -> FinancialAccount:
        return await self.repo.get(id)

    async def update_financial_account(self, id: int, payload: FinancialAccountUpdate) -> FinancialAccount:
        return await self.repo.update(id, payload)

    async def delete_financial_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_financial_accounts(self, clerk_user_id: str) -> dict:
        await self.plaid_account_service.sync_accounts(clerk_user_id)
        await self.snaptrade_account_service.sync_accounts(clerk_user_id)

        return {"message": "Financial accounts synced successfully"}
