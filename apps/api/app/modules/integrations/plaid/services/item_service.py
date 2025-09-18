from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from app.modules.integrations.plaid.schemas import PlaidItemCreate, PlaidItemUpdate, PaginatedPlaidItems
from app.db.models import PlaidItem
from app.clients.plaid_client import PlaidClient

class PlaidItemService:
    def __init__(self, session: AsyncSession, clerk_user_id: str):
        self.session = session
        self.clerk_user_id = clerk_user_id
        self.repo = PlaidItemRepo(session, clerk_user_id)
        self.plaid_client = PlaidClient(clerk_user_id)

    async def list_items(self, page: int, size: int) -> PaginatedPlaidItems:
        return await self.repo.paginate(page, size)
        
    async def create_item(self, payload: PlaidItemCreate) -> PlaidItem:
        return await self.repo.create(payload)

    async def get_item(self, id: int) -> PlaidItem:
        return await self.repo.get(id)

    async def update_item(self, id: int, payload: PlaidItemUpdate) -> PlaidItem:
        return await self.repo.update(id, payload)

    async def delete_item(self, id: int) -> dict:
        return await self.repo.delete(id)

    async def sync_items(self) -> dict:
        
        items_result = await self.repo.paginate(1, 100)

        if items_result.total == 0:
            return {"message": "No items to sync"}

        for item in items_result.items:
            ext_item = await self.plaid_client.get_item(item.access_token)
            payload = PlaidItemUpdate(
                clerk_user_id=self.clerk_user_id,
                item_id=ext_item.get("item_id"),
                institution_name=ext_item.get("institution_name"),
                access_token=item.access_token
            )
            await self.repo.update(item.id, payload)

        return {"message": "Items synced successfully"}