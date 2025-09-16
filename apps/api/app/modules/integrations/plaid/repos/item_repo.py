from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import PlaidItem
from app.modules.integrations.plaid.schemas import PlaidItemCreate, PlaidItemUpdate, PaginatedPlaidItems


class PlaidItemRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedPlaidItems:
        try:
            # Calculate offset for pagination
            offset = (page - 1) * size
            
            # Get total count for pagination metadata (SQLAlchemy 2.x)
            total_query = select(func.count()).select_from(PlaidItem)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            
            # Fetch only the items for the current page
            plaid_items_query = select(PlaidItem).offset(offset).limit(size)
            plaid_items_result = await self.session.execute(plaid_items_query)
            plaid_items = plaid_items_result.scalars().all()
            
            return PaginatedPlaidItems(items=plaid_items, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: PlaidItemCreate) -> PlaidItem:
        try:
            item = PlaidItem(clerk_user_id=payload.clerk_user_id, item_id=payload.item_id, access_token=payload.access_token, institution_name=payload.institution_name)
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
            return item
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> PlaidItem:
        try:
            item = await self.session.get(PlaidItem, id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: PlaidItemUpdate) -> PlaidItem:
        try:
            item = await self.session.get(PlaidItem, id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            item.item_id = payload.item_id
            item.access_token = payload.access_token
            item.clerk_user_id = payload.clerk_user_id
            item.institution_name = payload.institution_name
            await self.session.commit()
            await self.session.refresh(item)
            return item
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            item = await self.session.get(PlaidItem, id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            await self.session.delete(item)
            await self.session.commit()
            return {"message": "Item deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e

