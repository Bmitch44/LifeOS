import pytest
from types import SimpleNamespace

from app.modules.integrations.soundcloud.services.token_service import TokenService


@pytest.mark.anyio
async def test_crud_methods_call_repo(session, monkeypatch):
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")
    svc = TokenService(session, "test_user")

    class FakeRepo:
        async def create(self, payload): return SimpleNamespace(id=1, **payload.__dict__)
        async def get(self, _id): return SimpleNamespace(id=_id)
        async def update(self, _id, payload): return SimpleNamespace(id=_id, **payload.__dict__)
        async def delete(self, _id): return {"message": "ok"}

    monkeypatch.setattr(svc, "repo", FakeRepo())

    c = await svc.create_token(SimpleNamespace(clerk_user_id="test_user", access_token="a", token_type="b", expires_in=1, refresh_token="r", scope="*", expires_at=1))
    assert c.id == 1
    g = await svc.get_token(1)
    assert g.id == 1
    u = await svc.update_token(1, SimpleNamespace(clerk_user_id="test_user", access_token="a2", token_type="b", expires_in=1, refresh_token="r", scope="*", expires_at=1))
    assert u.access_token == "a2"
    d = await svc.delete_token(1)
    assert d["message"] == "ok"


