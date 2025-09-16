from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.snaptrade.models import SnaptradeAccount
from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate, SnaptradeAccountUpdate


class SnaptradeAccountRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

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
            account = await self.session.get(SnaptradeAccount, id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            return account
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SnaptradeAccountUpdate) -> SnaptradeAccount:
        try:
            account = await self.session.get(SnaptradeAccount, id)
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
            account = await self.session.get(SnaptradeAccount, id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")
            await self.session.delete(account)
            await self.session.commit()
            return {"message": "Account deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e