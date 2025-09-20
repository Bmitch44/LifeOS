import pytest
from types import SimpleNamespace

from app.modules.integrations.plaid.services.account_service import PlaidAccountService


class FakeRepo:
    def __init__(self):
        self.created = []
        self.updated = []

    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)

    async def create(self, payload):
        obj = SimpleNamespace(id=1, **payload.__dict__)
        self.created.append(obj)
        return obj

    async def get(self, id):
        return SimpleNamespace(id=id)

    async def update(self, id, payload):
        obj = SimpleNamespace(id=id, **payload.__dict__)
        self.updated.append(obj)
        return obj

    async def delete(self, id):
        return {"message": "Account deleted successfully"}

    async def get_by_account_id(self, account_id: str):
        return None


class FakeItemRepo:
    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)


class FakeFARepo:
    def __init__(self):
        self.created = []
        self.updated = []

    async def get_by_source_account_id(self, sid):
        return None

    async def create(self, payload):
        self.created.append(payload)
        return SimpleNamespace(id=1, **payload.__dict__)

    async def update(self, id, payload):
        self.updated.append((id, payload))
        return SimpleNamespace(id=id, **payload.__dict__)


class FakeMapper:
    def __init__(self, user):
        self.user = user

    def map_api_account_to_plaid_account(self, ext):
        return SimpleNamespace(
            clerk_user_id=self.user, account_id=ext.account_id, name=ext.name, official_name=None,
            type=ext.type, subtype=None, current_balance=ext.current_balance, available_balance=None,
            iso_currency_code=ext.iso_currency_code, mask=None,
        )

    def map_plaid_account_to_financial_account(self, acc):
        return SimpleNamespace(
            clerk_user_id=self.user, type=acc.type, name=acc.name, institution_name=None,
            currency=acc.iso_currency_code, current_balance=acc.current_balance, source="plaid", source_account_id=acc.account_id,
        )


class FakeClient:
    async def get_accounts(self, access_token: str):
        return [SimpleNamespace(account_id="a1", name="N", type="depository", current_balance=1.0, iso_currency_code="USD")]


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = PlaidAccountService(session, "test_user")
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "item_repo", FakeItemRepo())
    monkeypatch.setattr(svc, "financial_account_repo", FakeFARepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "plaid_client", FakeClient())

    page = await svc.list_accounts(1, 10)
    assert page.total == 0

    created = await svc.create_account(SimpleNamespace(clerk_user_id="test_user", account_id="a1", name="N"))
    assert created.id == 1

    got = await svc.get_account(1)
    assert got.id == 1

    updated = await svc.update_account(1, SimpleNamespace(clerk_user_id="test_user", account_id="a1", name="N2"))
    assert updated.name == "N2"

    res = await svc.delete_account(1)
    assert res["message"] == "Account deleted successfully"


@pytest.mark.anyio
async def test_sync_accounts_no_items(session, monkeypatch):
    svc = PlaidAccountService(session, "test_user")
    monkeypatch.setattr(svc, "item_repo", FakeItemRepo())
    res = await svc.sync_accounts()
    assert res["message"] == "No items to sync"


@pytest.mark.anyio
async def test_sync_accounts_creates_and_maps(session, monkeypatch):
    svc = PlaidAccountService(session, "test_user")
    fake_item_repo = FakeItemRepo()

    async def items(page, size):
        return SimpleNamespace(items=[SimpleNamespace(access_token="tok")], page=page, size=size, total=1)

    monkeypatch.setattr(fake_item_repo, "paginate", items)
    monkeypatch.setattr(svc, "item_repo", fake_item_repo)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "financial_account_repo", FakeFARepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "plaid_client", FakeClient())

    res = await svc.sync_accounts()
    assert res["message"] == "Accounts synced successfully"

