from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from app.modules.integrations.snaptrade.models import SnaptradeActivity
from app.modules.integrations.snaptrade.schemas import SnaptradeActivityCreate, SnaptradeActivityUpdate, PaginatedSnaptradeActivities


class SnaptradeActivityRepo:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id

    async def paginate(self, page: int, size: int) -> PaginatedSnaptradeActivities:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(SnaptradeActivity).where(SnaptradeActivity.clerk_user_id == self.clerk_user_id)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            activities_query = select(SnaptradeActivity).where(SnaptradeActivity.clerk_user_id == self.clerk_user_id).offset(offset).limit(size)
            activities_result = await self.session.execute(activities_query)
            activities = activities_result.scalars().all()
            return PaginatedSnaptradeActivities(items=activities, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: SnaptradeActivityCreate) -> SnaptradeActivity:
        try:
            activity = SnaptradeActivity(
                clerk_user_id=payload.clerk_user_id,
                account_id=payload.account_id,
                activity_id=payload.activity_id,
                symbol_id=payload.symbol_id,
                option_symbol_id=payload.option_symbol_id,
                type=payload.type,
                option_type=payload.option_type,
                price=payload.price,
                units=payload.units,
                amount=payload.amount,
                description=payload.description,
                trade_date=payload.trade_date,
                settlement_date=payload.settlement_date,
                currency=payload.currency,
                fees=payload.fees,
                fx_rate=payload.fx_rate,
                institution=payload.institution
            ) 
            self.session.add(activity)
            await self.session.commit()
            await self.session.refresh(activity)
            return activity
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> SnaptradeActivity:
        try:
            activity = await self.session.execute(
                select(SnaptradeActivity).where(SnaptradeActivity.id == id, SnaptradeActivity.clerk_user_id == self.clerk_user_id)
            )
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            return activity.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_activity_id(self, activity_id: str) -> SnaptradeActivity:
        try:
            activity = await self.session.execute(
                select(SnaptradeActivity).where(SnaptradeActivity.activity_id == activity_id, SnaptradeActivity.clerk_user_id == self.clerk_user_id)
            )
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            return activity.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: SnaptradeActivityUpdate) -> SnaptradeActivity:
        try:
            activity = await self.get(id)
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            activity.clerk_user_id = payload.clerk_user_id
            activity.account_id = payload.account_id
            activity.activity_id = payload.activity_id
            activity.symbol_id = payload.symbol_id
            activity.option_symbol_id = payload.option_symbol_id
            activity.type = payload.type
            activity.option_type = payload.option_type
            activity.price = payload.price
            activity.units = payload.units
            activity.amount = payload.amount
            activity.description = payload.description
            activity.trade_date = payload.trade_date
            activity.settlement_date = payload.settlement_date
            activity.currency = payload.currency
            activity.fees = payload.fees
            activity.fx_rate = payload.fx_rate
            activity.institution = payload.institution
            await self.session.commit()
            await self.session.refresh(activity)
            return activity
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            activity = await self.get(id)
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            await self.session.delete(activity)
            await self.session.commit()
            return {"message": "Activity deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e