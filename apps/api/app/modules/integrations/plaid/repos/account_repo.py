from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import PlaidAccount
from app.modules.integrations.plaid.schemas import PlaidAccountCreate, PlaidAccountUpdate, PaginatedPlaidAccounts


class PlaidAccountRepo:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id

    async def paginate(self, page: int, size: int) -> PaginatedPlaidAccounts:
        try:
            # Calculate offset for pagination
            offset = (page - 1) * size
            
            # Get total count for pagination metadata (SQLAlchemy 2.x)
            total_query = select(func.count()).select_from(PlaidAccount).where(PlaidAccount.clerk_user_id == self.clerk_user_id)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            
            # Fetch only the accounts for the current page
            plaid_accounts_query = select(PlaidAccount).where(PlaidAccount.clerk_user_id == self.clerk_user_id).offset(offset).limit(size)
            plaid_accounts_result = await self.session.execute(plaid_accounts_query)
            plaid_accounts = plaid_accounts_result.scalars().all()
            
            return PaginatedPlaidAccounts(items=plaid_accounts, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: PlaidAccountCreate) -> PlaidAccount:
        try:
            account = PlaidAccount(
                clerk_user_id=payload.clerk_user_id, 
                account_id=payload.account_id, 
                name=payload.name, 
                official_name=payload.official_name, 
                type=payload.type, 
                subtype=payload.subtype, 
                current_balance=payload.current_balance, 
                available_balance=payload.available_balance, 
                iso_currency_code=payload.iso_currency_code, 
                mask=payload.mask
            )
            self.session.add(account)
            await self.session.commit()
            await self.session.refresh(account)
            return account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> PlaidAccount:
        try:
            account = await self.session.execute(
                select(PlaidAccount).where(PlaidAccount.id == id, PlaidAccount.clerk_user_id == self.clerk_user_id)
            )
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            return account.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_account_id(self, account_id: str) -> PlaidAccount:
        try:
            account = await self.session.execute(
                select(PlaidAccount).where(PlaidAccount.account_id == account_id, PlaidAccount.clerk_user_id == self.clerk_user_id)
            )
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            return account.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: PlaidAccountUpdate) -> PlaidAccount:
        try:
            account = await self.get(id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            account.account_id = payload.account_id
            account.name = payload.name
            account.official_name = payload.official_name
            account.type = payload.type
            account.subtype = payload.subtype
            account.current_balance = payload.current_balance
            account.available_balance = payload.available_balance
            account.iso_currency_code = payload.iso_currency_code
            account.mask = payload.mask
            await self.session.commit()
            await self.session.refresh(account)
            return account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            account = await self.get(id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            await self.session.delete(account)
            await self.session.commit()
            return {"message": "Account deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e

