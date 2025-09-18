from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from app.modules.integrations.snaptrade.models import SnaptradeAccount
from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate, PaginatedSnaptradeAccounts


class SnaptradeAccountRepo:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id

    async def paginate(self, page: int, size: int) -> PaginatedSnaptradeAccounts:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(SnaptradeAccount).where(SnaptradeAccount.clerk_user_id == self.clerk_user_id)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            accounts_query = select(SnaptradeAccount).where(SnaptradeAccount.clerk_user_id == self.clerk_user_id).offset(offset).limit(size)
            accounts_result = await self.session.execute(accounts_query)
            accounts = accounts_result.scalars().all()
            return PaginatedSnaptradeAccounts(items=accounts, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: SnaptradeAccountCreate) -> SnaptradeAccount:
        try:
            account = SnaptradeAccount(
                clerk_user_id=payload.clerk_user_id,
                account_id=payload.account_id,
                connection_id=payload.connection_id,
                name=payload.name,
                number=payload.number,
                institution_name=payload.institution_name,
                status=payload.status,
                type=payload.type,
                current_balance=payload.current_balance,
                currency=payload.currency
            ) 
            self.session.add(account)
            await self.session.commit()
            await self.session.refresh(account)
            return account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> SnaptradeAccount:
        try:
            account = await self.session.execute(
                select(SnaptradeAccount).where(SnaptradeAccount.id == id, SnaptradeAccount.clerk_user_id == self.clerk_user_id)
            )
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            return account.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_account_id(self, account_id: str) -> SnaptradeAccount:
        try:
            account = await self.session.execute(
                select(SnaptradeAccount).where(SnaptradeAccount.account_id == account_id, SnaptradeAccount.clerk_user_id == self.clerk_user_id)
            )
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            return account.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SnaptradeAccountUpdate) -> SnaptradeAccount:
        try:
            account = await self.get(id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            account.clerk_user_id = payload.clerk_user_id
            account.account_id = payload.account_id
            account.connection_id = payload.connection_id
            account.name = payload.name
            account.number = payload.number
            account.institution_name = payload.institution_name
            account.status = payload.status
            account.type = payload.type
            account.current_balance = payload.current_balance
            account.currency = payload.currency
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