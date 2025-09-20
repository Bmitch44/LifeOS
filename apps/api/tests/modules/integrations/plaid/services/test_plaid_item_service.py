import pytest
from types import SimpleNamespace

from app.modules.integrations.plaid.services.item_service import PlaidItemService


class FakeRepo:
    def __init__(self):
        self.updated = []

    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)

    async def create(self, payload):
        return SimpleNamespace(id=1, **payload.__dict__)

    async def get(self, id):
        return SimpleNamespace(id=id)

    async def update(self, id, payload):
        self.updated.append((id, payload))
        return SimpleNamespace(id=id, **payload.__dict__)

    async def delete(self, id):
        return {"message": "Item deleted successfully"}


class FakeClient:
    async def get_item(self, access_token: str):
        return {"item_id": "item_ext", "institution_name": "Inst"}


@pytest.mark.anyio
async def test_list_items_unit(session, monkeypatch):
    svc = PlaidItemService(session, "test_user")
    fake_repo = FakeRepo()
    monkeypatch.setattr(svc, "repo", fake_repo)
    page = await svc.list_items(1, 10)
    assert page.total == 0


@pytest.mark.anyio
async def test_create_get_update_delete_unit(session, monkeypatch):
    svc = PlaidItemService(session, "test_user")
    fake_repo = FakeRepo()
    monkeypatch.setattr(svc, "repo", fake_repo)

    created = await svc.create_item(SimpleNamespace(
        clerk_user_id="test_user", item_id="i1", access_token="t1", institution_name="Inst"
    ))
    assert created.id == 1

    got = await svc.get_item(1)
    assert got.id == 1

    updated = await svc.update_item(1, SimpleNamespace(
        clerk_user_id="test_user", item_id="i1", access_token="t2", institution_name="New"
    ))
    assert updated.access_token == "t2"

    res = await svc.delete_item(1)
    assert res["message"] == "Item deleted successfully"


@pytest.mark.anyio
async def test_sync_items_no_items(session, monkeypatch):
    svc = PlaidItemService(session, "test_user")
    fake_repo = FakeRepo()
    monkeypatch.setattr(svc, "repo", fake_repo)
    res = await svc.sync_items()
    assert res["message"] == "No items to sync"


@pytest.mark.anyio
async def test_sync_items_updates(session, monkeypatch):
    svc = PlaidItemService(session, "test_user")
    fake_repo = FakeRepo()

    async def paginate_with_items(page, size):
        # one existing item with access token
        return SimpleNamespace(items=[SimpleNamespace(id=1, access_token="tok")], page=page, size=size, total=1)

    monkeypatch.setattr(fake_repo, "paginate", paginate_with_items)
    monkeypatch.setattr(svc, "repo", fake_repo)
    monkeypatch.setattr(svc, "plaid_client", FakeClient())

    res = await svc.sync_items()
    assert res["message"] == "Items synced successfully"
    assert len(fake_repo.updated) == 1


