import pytest
from types import SimpleNamespace

from app.modules.integrations.snaptrade.services.connection_service import SnaptradeConnectionService


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
        return {"message": "Connection deleted successfully"}

    async def get_by_connection_id(self, cid):
        return None


class FakeMapper:
    def __init__(self, user): self.user = user
    def map_api_connection_to_snaptrade_connection(self, ext, user_secret):
        return SimpleNamespace(
            clerk_user_id=self.user,
            user_secret=user_secret,
            connection_id=ext.get("id"),
            brokerage_name=ext.get("name"),
        )


class FakeClient:
    def get_connections(self, user_secret: str):
        return [{"id": "c1", "name": "Broker"}]


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = SnaptradeConnectionService(session, "test_user")
    monkeypatch.setattr(svc, "repo", FakeRepo())
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    page = await svc.list_connections(1, 10)
    assert page.total == 0

    created = await svc.create_connection(SimpleNamespace(clerk_user_id="test_user"))
    assert created.id == 1

    got = await svc.get_connection(1)
    assert got.id == 1

    updated = await svc.update_connection(1, SimpleNamespace(clerk_user_id="test_user"))
    assert updated.id == 1

    res = await svc.delete_connection(1)
    assert res["message"] == "Connection deleted successfully"


@pytest.mark.anyio
async def test_sync_connections_no_connections(session, monkeypatch):
    svc = SnaptradeConnectionService(session, "test_user")
    monkeypatch.setattr(svc, "repo", FakeRepo())
    res = await svc.sync_connections()
    assert res["message"] == "No connections to sync"


@pytest.mark.anyio
async def test_sync_connections_upsert(session, monkeypatch):
    svc = SnaptradeConnectionService(session, "test_user")
    fake_repo = FakeRepo()
    async def conns(page, size):
        return SimpleNamespace(items=[SimpleNamespace(user_secret="usec")], page=page, size=size, total=1)
    monkeypatch.setattr(fake_repo, "paginate", conns)

    monkeypatch.setattr(svc, "repo", fake_repo)
    monkeypatch.setattr(svc, "mapper", FakeMapper("test_user"))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient())

    res = await svc.sync_connections()
    assert res["message"] == "Connections synced successfully"


