import pytest
from types import SimpleNamespace

from app.modules.users.service import UsersService


class FakeRepo:
    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)

    async def get(self, id):
        return SimpleNamespace(id=id)

    async def update(self, id, payload):
        return SimpleNamespace(id=id, **payload.__dict__)

    async def delete(self, id):
        return {"message": "User deleted successfully"}


@pytest.mark.anyio
async def test_list_get_update_delete_unit(session, monkeypatch):
    svc = UsersService(session)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    page = await svc.list_users(1, 10)
    assert page.total == 0

    got = await svc.get_user(1)
    assert got.id == 1

    updated = await svc.update_user(1, SimpleNamespace(email="n@ex.com", first_name="N", last_name="L", phone="123"))
    assert updated.email == "n@ex.com"

    res = await svc.delete_user(1)
    assert res["message"] == "User deleted successfully"


