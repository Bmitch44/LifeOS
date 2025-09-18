import pytest


@pytest.fixture
def mock_plaid(monkeypatch):
    from app.clients.plaid_client import PlaidClient
    def _apply(
        link_token="link-token-123",
        item=None,
        accounts=None,
        exchange=None,
    ):
        if link_token is not None:
            async def _create_link_token(self, clerk_user_id: str):
                return {"link_token": link_token}
            monkeypatch.setattr(PlaidClient, "create_link_token", _create_link_token, raising=False)
        if exchange is not None:
            async def _exchange(self, public_token: str):
                return exchange
            monkeypatch.setattr(PlaidClient, "exchange_public_token", _exchange, raising=False)
        if item is not None:
            async def _get_item(self, access_token: str):
                return item
            monkeypatch.setattr(PlaidClient, "get_item", _get_item, raising=False)
        if accounts is not None:
            async def _get_accounts(self, access_token: str):
                return accounts
            monkeypatch.setattr(PlaidClient, "get_accounts", _get_accounts, raising=False)
    return _apply


@pytest.fixture
def mock_snaptrade(monkeypatch):
    from app.clients.snaptrade_client import SnaptradeClient
    def _apply(
        users=None,
        connections=None,
        accounts=None,
        register=None,
        portal="http://redirect",
    ):
        async def _portal(self, clerk_user_id: str):
            return portal
        monkeypatch.setattr(SnaptradeClient, "create_connection_portal", _portal, raising=False)

        if register is not None:
            def _register(self, clerk_user_id: str):
                return register
            monkeypatch.setattr(SnaptradeClient, "register_user", _register, raising=False)
        if connections is not None:
            def _connections(self, clerk_user_id: str, snaptrade_user_secret: str):
                return connections
            monkeypatch.setattr(SnaptradeClient, "get_connections", _connections, raising=False)
        if accounts is not None:
            def _accounts(self, clerk_user_id: str, snaptrade_user_secret: str):
                return accounts
            monkeypatch.setattr(SnaptradeClient, "get_accounts", _accounts, raising=False)
        if users is not None:
            def _users(self):
                return users
            monkeypatch.setattr(SnaptradeClient, "get_users", _users, raising=False)
    return _apply