from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from app.modules.integrations.plaid.schemas import PlaidItemCreate, PlaidItemUpdate, PaginatedPlaidItems
from app.db.models import PlaidItem
from app.clients.plaid_client import PlaidClient

class PlaidItemService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PlaidItemRepo(session)
        self.plaid_client = PlaidClient()

    async def list_items(self, clerk_user_id: str, page: int, size: int) -> PaginatedPlaidItems:
        return await self.repo.paginate(clerk_user_id, page, size)
        
    async def create_item(self, payload: PlaidItemCreate) -> PlaidItem:
        return await self.repo.create(payload)

    async def get_item(self, id: int) -> PlaidItem:
        return await self.repo.get(id)

    async def update_item(self, id: int, payload: PlaidItemUpdate) -> PlaidItem:
        return await self.repo.update(id, payload)

    async def delete_item(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_items(self, clerk_user_id: str) -> dict:
        
        # Fetch all Plaid items to get their access tokens
        items_result = await self.session.execute(select(PlaidItem).where(PlaidItem.clerk_user_id == clerk_user_id))
        items = items_result.scalars().all()

        # If no items, return
        if not items:
            return {"message": "No items to sync"}

        # Update each item with the new item_id and institution_name
        for item in items:
            ext_item = await self.plaid_client.get_item(item.access_token)
            item.item_id = ext_item.get("item_id")
            item.institution_name = ext_item.get("institution_name")
            await self.repo.update(item.id, item)

        return {"message": "Items synced successfully"}