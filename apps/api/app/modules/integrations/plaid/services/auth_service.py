from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.plaid_client import PlaidClient
from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from app.modules.integrations.plaid.schemas import PlaidItemCreate
from app.db.models import PlaidItem


class PlaidAuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.plaid_client = PlaidClient()
        self.plaid_item_repo = PlaidItemRepo(session)

    async def get_link_token(self, clerk_user_id: str) -> str:
        link_token_response = await self.plaid_client.create_link_token(clerk_user_id)
        link_token = link_token_response.get("link_token")
        return link_token

    async def exchange_public_token(self, clerk_user_id: str, public_token: str) -> PlaidItem:
        if not public_token:
            raise HTTPException(status_code=400, detail="Public token is required")
            
        exchange_response = await self.plaid_client.exchange_public_token(public_token)

        access_token = exchange_response.get("access_token")
        item_id = exchange_response.get("item_id")
        payload = PlaidItemCreate(
            clerk_user_id=clerk_user_id,
            item_id=item_id,
            access_token=access_token,
            institution_name=None,
        )
        return await self.plaid_item_repo.create(payload)