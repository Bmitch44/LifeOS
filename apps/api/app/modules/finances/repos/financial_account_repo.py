from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.modules.finances.schemas import PaginatedFinancialAccounts, FinancialAccountUpdate, FinancialAccountCreate
from app.db.models import FinancialAccount  


class FinancialAccountRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, clerk_user_id: str, page: int, size: int) -> PaginatedFinancialAccounts:
        try:
            # Calculate offset for pagination
            offset = (page - 1) * size
            
            # Get total count for pagination metadata (SQLAlchemy 2.x)
            total_query = select(func.count()).select_from(FinancialAccount).where(FinancialAccount.clerk_user_id == clerk_user_id)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            
            # Fetch only the users for the current page
            financial_accounts_query = select(FinancialAccount).where(FinancialAccount.clerk_user_id == clerk_user_id).offset(offset).limit(size)
            financial_accounts_result = await self.session.execute(financial_accounts_query)
            financial_accounts = financial_accounts_result.scalars().all()
            
            return PaginatedFinancialAccounts(items=financial_accounts, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: FinancialAccountCreate) -> FinancialAccount:
        try:
            financial_account = FinancialAccount(
                clerk_user_id=payload.clerk_user_id,
                type=payload.type,
                name=payload.name,
                institution_name=payload.institution_name,
                currency=payload.currency,
                current_balance=payload.current_balance,
                source=payload.source,
                source_account_id=payload.source_account_id
            )
            self.session.add(financial_account)
            await self.session.commit()
            await self.session.refresh(financial_account)
            return financial_account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> FinancialAccount:
        try:
            financial_account = await self.session.get(FinancialAccount, id)
            if not financial_account:
                raise HTTPException(status_code=404, detail="Financial account not found")
            return financial_account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_source_account_id(self, source_account_id: str) -> FinancialAccount:
        try:
            financial_account = await self.session.execute(select(FinancialAccount).where(FinancialAccount.source_account_id == source_account_id))
            if not financial_account:
                raise HTTPException(status_code=404, detail="Financial account not found")
            return financial_account.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: FinancialAccountUpdate) -> FinancialAccount:
        try:
            financial_account = await self.session.get(FinancialAccount, id)
            if not financial_account:
                raise HTTPException(status_code=404, detail="Financial account not found")
            financial_account.clerk_user_id = payload.clerk_user_id
            financial_account.type = payload.type
            financial_account.name = payload.name
            financial_account.institution_name = payload.institution_name
            financial_account.currency = payload.currency
            financial_account.current_balance = payload.current_balance
            financial_account.source = payload.source
            financial_account.source_account_id = payload.source_account_id
            await self.session.commit()
            await self.session.refresh(financial_account)
            return financial_account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            financial_account = await self.session.get(FinancialAccount, id)
            if not financial_account:
                raise HTTPException(status_code=404, detail="Financial account not found")
            await self.session.execute(delete(FinancialAccount).where(FinancialAccount.id == id))
            await self.session.commit()
            return {"message": "Financial account deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e


