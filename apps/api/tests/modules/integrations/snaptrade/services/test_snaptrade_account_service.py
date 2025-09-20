import pytest
from types import SimpleNamespace

from app.modules.integrations.snaptrade.services.account_service import SnaptradeAccountService


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


class FakeConnRepo:
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
    def __init__(self, user): self.user = user
    def map_api_account_to_snaptrade_account(self, ext):
        return SimpleNamespace(
            clerk_user_id=self.user,
            account_id=ext.get("id"),
            connection_id=ext.get("brokerage_authorization"),
            name=ext.get("name"),
            number=ext.get("number"),
            institution_name=ext.get("institution_name"),
            status=ext.get("status"),
            type=ext.get("raw_type"),
            current_balance=ext.get("balance", {}).get("total", {}).get("amount", 0),
            currency=ext.get("balance", {}).get("total", {}).get("currency", "CAD"),
        )
    def map_snaptrade_account_to_financial_account(self, acc):
        return SimpleNamespace(
            clerk_user_id=self.user, type=acc.type, name=acc.name, institution_name=acc.institution_name,
            currency=acc.currency, current_balance=acc.current_balance, source="snaptrade", source_account_id=acc.account_id,
        )


class FakeClient:
    def get_accounts(self, user_secret: str):
        return [{
            "id": "s1",
            "brokerage_authorization": "c1",
            "name": "N",
            "number": "1",
            "institution_name": "Inst",
            "status": "active",
            "raw_type": "cash",
            "balance": {"total": {"amount": 10.0, "currency": "USD"}},
        }]


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = SnaptradeAccountService(session, "test_user")
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "connection_repo", FakeConnRepo())
    monkeypatch.setattr(svc, "financial_account_repo", FakeFARepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    page = await svc.list_accounts(1, 10)
    assert page.total == 0

    created = await svc.create_account(SimpleNamespace(clerk_user_id="test_user", account_id="s1", name="N"))
    assert created.id == 1

    got = await svc.get_account(1)
    assert got.id == 1

    updated = await svc.update_account(1, SimpleNamespace(clerk_user_id="test_user", account_id="s1", name="N2"))
    assert updated.name == "N2"

    res = await svc.delete_account(1)
    assert res["message"] == "Account deleted successfully"


@pytest.mark.anyio
async def test_sync_accounts_no_connections(session, monkeypatch):
    svc = SnaptradeAccountService(session, "test_user")
    monkeypatch.setattr(svc, "connection_repo", FakeConnRepo())
    res = await svc.sync_accounts()
    assert res["message"] == "No connections to sync"


@pytest.mark.anyio
async def test_sync_accounts_creates_and_maps(session, monkeypatch):
    svc = SnaptradeAccountService(session, "test_user")
    fake_conn_repo = FakeConnRepo()
    async def conns(page, size):
        return SimpleNamespace(items=[SimpleNamespace(user_secret="usec")], page=page, size=size, total=1)
    monkeypatch.setattr(fake_conn_repo, "paginate", conns)

    monkeypatch.setattr(svc, "connection_repo", fake_conn_repo)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "financial_account_repo", FakeFARepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    res = await svc.sync_accounts()
    assert res["message"] == "Accounts synced successfully"


