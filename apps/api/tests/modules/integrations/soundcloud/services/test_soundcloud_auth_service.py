import pytest
from types import SimpleNamespace

from app.modules.integrations.soundcloud.services.auth_service import SoundcloudAuthService


class FakeTokenRepo:
    def __init__(self, existing=None):
        self._existing = existing
        self.created = []
        self.updated = []

    async def get_by_clerk_user_id(self):
        return self._existing

    async def create(self, payload):
        obj = SimpleNamespace(id=1, **payload.__dict__)
        self.created.append(obj)
        return obj

    async def update(self, _id, payload):
        obj = SimpleNamespace(id=_id, **payload.__dict__)
        self.updated.append(obj)
        return obj


class FakeClient:
    def __init__(self):
        pass

    def build_authorize_url(self):
        return ("http://auth", "verifier", "state")

    def exchange_code_for_token(self, **kwargs):
        return {"access_token": "a", "token_type": "bearer", "expires_in": 3600, "refresh_token": "r", "scope": "*", "expires_at": 123}

    def refresh_access_token(self, **kwargs):
        return {"access_token": "a2", "token_type": "bearer", "expires_in": 3600, "refresh_token": "r2", "scope": "*", "expires_at": 456}


@pytest.mark.anyio
async def test_get_authorize_url(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = SoundcloudAuthService(session, "test_user")
    monkeypatch.setattr(svc, "client", FakeClient())
    url = await svc.get_authorize_url()
    assert "authorize_url" in url and "code_verifier" in url and "state" in url


@pytest.mark.anyio
async def test_exchange_code_creates_when_missing(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = SoundcloudAuthService(session, "test_user")
    monkeypatch.setattr(svc, "client", FakeClient())
    repo = FakeTokenRepo(None)
    monkeypatch.setattr(svc, "token_repo", repo)
    res = await svc.exchange_code(code="c", code_verifier="v")
    assert "token_id" in res
    assert len(repo.created) == 1


@pytest.mark.anyio
async def test_exchange_code_updates_when_exists(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = SoundcloudAuthService(session, "test_user")
    monkeypatch.setattr(svc, "client", FakeClient())
    repo = FakeTokenRepo(SimpleNamespace(id=2, refresh_token="r"))
    monkeypatch.setattr(svc, "token_repo", repo)
    res = await svc.exchange_code(code="c", code_verifier="v")
    assert "token_id" in res
    assert len(repo.updated) == 1


@pytest.mark.anyio
async def test_refresh_updates_token(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = SoundcloudAuthService(session, "test_user")
    monkeypatch.setattr(svc, "client", FakeClient())
    repo = FakeTokenRepo(SimpleNamespace(id=3, refresh_token="rOld"))
    monkeypatch.setattr(svc, "token_repo", repo)
    res = await svc.refresh()
    assert "token_id" in res
    assert len(repo.updated) == 1


