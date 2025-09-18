from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from app.modules.finances.schemas import FinancialAccountCreate, FinancialAccountUpdate, PaginatedFinancialAccounts
from app.modules.finances.models import FinancialAccount
from app.modules.integrations.plaid.services import PlaidAccountService
from app.modules.integrations.snaptrade.services import SnaptradeAccountService


class FinancialAccountService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.repo = FinancialAccountRepo(session, clerk_user_id)
        self.plaid_account_service = PlaidAccountService(session, clerk_user_id)
        self.snaptrade_account_service = SnaptradeAccountService(session, clerk_user_id)

    async def list_financial_accounts(self, page: int, size: int) -> PaginatedFinancialAccounts:
        return await self.repo.paginate(page, size)
        
    async def create_financial_account(self, payload: FinancialAccountCreate) -> FinancialAccount:
        return await self.repo.create(payload)

    async def get_financial_account(self, id: int) -> FinancialAccount:
        return await self.repo.get(id)

    async def update_financial_account(self, id: int, payload: FinancialAccountUpdate) -> FinancialAccount:
        return await self.repo.update(id, payload)

    async def delete_financial_account(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_financial_accounts(self) -> dict:
        await self.plaid_account_service.sync_accounts()
        await self.snaptrade_account_service.sync_accounts()

        return {"message": "Financial accounts synced successfully"}
