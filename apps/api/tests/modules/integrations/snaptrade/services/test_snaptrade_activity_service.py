import pytest
from types import SimpleNamespace

from app.modules.integrations.snaptrade.services.activity_service import SnaptradeActivityService


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
        return {"message": "Activity deleted successfully"}

    async def get_by_activity_id(self, activity_id: str):
        return None


class FakeConnRepo:
    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)


class FakeMapper:
    def __init__(self, user): self.user = user
    def map_api_account_to_snaptrade_account(self, ext, account_id):
        return SimpleNamespace(
            clerk_user_id=self.user,
            account_id=account_id,
            activity_id=ext.get("id"),
            symbol_id=None,
            option_symbol_id=None,
            type=ext.get("type"),
            option_type=ext.get("option_type"),
            price=ext.get("price", 0),
            units=ext.get("units", 0),
            amount=ext.get("amount"),
            description=ext.get("description", ""),
            trade_date=ext.get("trade_date"),
            settlement_date=ext.get("settlement_date"),
            currency=ext.get("currency", "CAD"),
            fees=ext.get("fee", 0),
            fx_rate=ext.get("fx_rate"),
            institution=ext.get("institution", ""),
        )


class FakeClient:
    def get_account_activities(self, user_secret: str, account_id: str):
        return [{
            "id": "a1",
            "type": "trade",
            "price": 10.0,
            "units": 1,
            "amount": 10.0,
            "description": "Buy",
            "currency": {"code": "USD"},
        }]


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = SnaptradeActivityService(session, "test_user")
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "connection_repo", FakeConnRepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    page = await svc.list_activities(1, 10)
    assert page.total == 0

    created = await svc.create_activity(SimpleNamespace(clerk_user_id="test_user", account_id="acc", activity_id="a1"))
    assert created.id == 1

    got = await svc.get_activity(1)
    assert got.id == 1

    updated = await svc.update_activity(1, SimpleNamespace(clerk_user_id="test_user", account_id="acc", activity_id="a1"))
    assert updated.id == 1

    res = await svc.delete_activity(1)
    assert res["message"] == "Activity deleted successfully"


@pytest.mark.anyio
async def test_sync_activities_no_connections(session, monkeypatch):
    svc = SnaptradeActivityService(session, "test_user")
    monkeypatch.setattr(svc, "connection_repo", FakeConnRepo())
    res = await svc.sync_activities("acc_1")
    assert res["message"] == "No connections to sync"


@pytest.mark.anyio
async def test_sync_activities_creates(session, monkeypatch):
    svc = SnaptradeActivityService(session, "test_user")
    fake_conn_repo = FakeConnRepo()
    async def conns(page, size):
        return SimpleNamespace(items=[SimpleNamespace(user_secret="usec")], page=page, size=size, total=1)
    monkeypatch.setattr(fake_conn_repo, "paginate", conns)

    monkeypatch.setattr(svc, "connection_repo", fake_conn_repo)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    res = await svc.sync_activities("acc_1")
    assert res["message"] == "Activities synced successfully"


