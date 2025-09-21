import pytest
from types import SimpleNamespace

from app.modules.integrations.snaptrade.services.auth_service import SnaptradeAuthService


class FakeConnRepo:
    def __init__(self, existing=None):
        self._existing = existing
        self.created = []

    async def get_by_clerk_user_id(self):
        return self._existing

    async def create(self, payload):
        obj = SimpleNamespace(id=1, **payload.__dict__)
        self.created.append(obj)
        return obj


class FakeClient:
    def __init__(self, redirect="http://redirect"): self._redirect = redirect
    def get_all_users(self): return {"users": []}
    def register_user(self): return {"user_secret": "secret_1", "user_id": "u1"}
    def create_connection_portal(self, user_secret: str): return self._redirect


@pytest.mark.anyio
async def test_get_connection_portal_existing_connection(session, monkeypatch):
    svc = SnaptradeAuthService(session, "test_user")
    existing = SimpleNamespace(user_secret="secret_1")
    monkeypatch.setattr(svc, "snaptrade_connection_repo", FakeConnRepo(existing))
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient("http://ok"))
    url = await svc.get_connection_portal()
    assert url == "http://ok"


@pytest.mark.anyio
async def test_get_connection_portal_creates_when_missing(session, monkeypatch):
    svc = SnaptradeAuthService(session, "test_user")
    repo = FakeConnRepo(None)
    monkeypatch.setattr(svc, "snaptrade_connection_repo", repo)
    monkeypatch.setattr(svc, "snaptrade_client", FakeClient("http://ok"))
    url = await svc.get_connection_portal()
    assert url == "http://ok"
    assert len(repo.created) == 1


