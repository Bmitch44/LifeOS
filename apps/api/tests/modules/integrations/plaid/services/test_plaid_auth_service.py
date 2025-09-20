import pytest
from types import SimpleNamespace

from app.modules.integrations.plaid.services.auth_service import PlaidAuthService


class FakeClient:
    async def create_link_token(self):
        return {"link_token": "ltok"}

    async def exchange_public_token(self, public_token: str):
        return {"access_token": "atok", "item_id": "iid"}


class FakeRepo:
    async def create(self, payload):
        return SimpleNamespace(id=1, **payload.__dict__)


@pytest.mark.anyio
async def test_get_link_token_unit(session, monkeypatch):
    svc = PlaidAuthService(session, "test_user")
    monkeypatch.setattr(svc, "plaid_client", FakeClient())
    token = await svc.get_link_token()
    assert token == "ltok"


@pytest.mark.anyio
async def test_exchange_public_token_unit(session, monkeypatch):
    svc = PlaidAuthService(session, "test_user")
    monkeypatch.setattr(svc, "plaid_client", FakeClient())
    monkeypatch.setattr(svc, "plaid_item_repo", FakeRepo())
    item = await svc.exchange_public_token("public-token")
    assert item.id == 1


