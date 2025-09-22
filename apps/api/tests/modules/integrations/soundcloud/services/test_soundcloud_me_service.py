import pytest
from types import SimpleNamespace

from app.modules.integrations.soundcloud.services.me_service import MeService


class FakeClient:
    def __init__(self, me):
        self._me = me

    def get_me(self, token):
        return self._me


@pytest.mark.anyio
async def test_sync_me_creates_when_missing(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = MeService(session, "test_user")
    api_me = {"username": "user", "urn": "u"}
    monkeypatch.setattr(svc, "soundcloud_client", FakeClient(api_me))
    # ensure no existing: repo.get_by_clerk_user_id would raise 404 in current repo; we bypass by monkeypatch repo
    class FakeRepo:
        def __init__(self):
            self.created = []
        async def get_by_clerk_user_id(self):
            return None
        async def create(self, payload):
            obj = SimpleNamespace(id=1, **payload.__dict__)
            self.created.append(obj)
            return obj
        async def update(self, *_):
            raise AssertionError("should not update")
    repo = FakeRepo()
    monkeypatch.setattr(svc, "repo", repo)
    res = await svc.sync_me()
    assert res.id == 1
    assert len(repo.created) == 1


@pytest.mark.anyio
async def test_sync_me_updates_when_exists(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = MeService(session, "test_user")
    api_me = {"username": "user2", "urn": "u2"}
    monkeypatch.setattr(svc, "soundcloud_client", FakeClient(api_me))
    class FakeRepo:
        def __init__(self):
            self.updated = []
        async def get_by_clerk_user_id(self):
            return SimpleNamespace(id=2)
        async def create(self, *_):
            raise AssertionError("should not create")
        async def update(self, _id, payload):
            obj = SimpleNamespace(id=_id, **payload.__dict__)
            self.updated.append(obj)
            return obj
    repo = FakeRepo()
    monkeypatch.setattr(svc, "repo", repo)
    res = await svc.sync_me()
    assert res.id == 2
    assert len(repo.updated) == 1


