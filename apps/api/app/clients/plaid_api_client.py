from enum import Enum

from fastapi import HTTPException
from plaid.model.item_with_consent_fields import ItemWithConsentFields
from app.settings import settings
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_response import LinkTokenCreateResponse
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.item_public_token_exchange_response import ItemPublicTokenExchangeResponse
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.item_get_response import ItemGetResponse
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_get_response import AccountsGetResponse
from plaid.model.account_base import AccountBase

class PlaidConnectionType(Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"

class PlaidClient:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id
        self.client = self._setup_plaid_client(PlaidConnectionType.PRODUCTION)

    def _setup_plaid_client(self, connection_type: PlaidConnectionType):
        host = plaid.Environment.Production if connection_type == PlaidConnectionType.PRODUCTION else plaid.Environment.Sandbox
        config = plaid.Configuration(
            host=host,
            api_key={
                'clientId': settings.plaid_client_id,
                'secret': settings.plaid_prod_secret if connection_type == PlaidConnectionType.PRODUCTION else settings.plaid_sandbox_secret,
            }
        )
        api_client = plaid.ApiClient(config)
        return plaid_api.PlaidApi(api_client)

    async def create_link_token(self) -> dict:
        """Create a link token for Plaid Link initialization"""
        try:
            # Request only necessary products to improve conversion and cost
            products = [Products("transactions")]

            # Use CA by default to enable more Link flows (e.g., Instant Match)
            country_codes = [CountryCode('US'), CountryCode('CA')]

            request = LinkTokenCreateRequest(
                products=products,
                client_name="LifeOS",
                country_codes=country_codes,
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=str(self.clerk_user_id)),
                redirect_uri=settings.plaid_redirect_uri if getattr(settings, 'plaid_redirect_uri', None) else None,
            )
            response: LinkTokenCreateResponse = self.client.link_token_create(link_token_create_request=request)
            return {"link_token": response.link_token}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

    async def exchange_public_token(self, public_token: str) -> dict:
        """Exchange public token for access token and initialize account data"""
        try:
            exchange_request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            exchange_response: ItemPublicTokenExchangeResponse = self.client.item_public_token_exchange(exchange_request)
            return {"access_token": exchange_response.access_token, "item_id": exchange_response.item_id}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

    async def get_item(self, access_token: str) -> ItemWithConsentFields:
        """Get item details"""
        try:
            item_request = ItemGetRequest(access_token=access_token)
            item_response: ItemGetResponse = self.client.item_get(item_get_request=item_request)
            return item_response.item
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

    async def get_accounts(self, access_token: str) -> list[AccountBase]:
        """Get accounts"""
        try:
            accounts_request = AccountsGetRequest(access_token=access_token)
            accounts_response: AccountsGetResponse = self.client.accounts_get(accounts_request)
            return accounts_response.accounts
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))