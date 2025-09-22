import pytest
from datetime import datetime, timedelta

from app.modules.integrations.soundcloud.repos.token_repo import TokenRepo


@pytest.mark.anyio
async def test_create_get_update_delete(session):
    repo = TokenRepo(session, clerk_user_id="test_user")
    created = await repo.create(type("Obj", (), {
        "clerk_user_id": "test_user",
        "access_token": "a",
        "token_type": "bearer",
        "expires_in": 3600,
        "refresh_token": "r",
        "scope": "*",
        "expires_at": datetime.utcnow() + timedelta(hours=1),
    })())
    assert created.id is not None

    got = await repo.get(created.id)
    assert got.id == created.id

    got2 = await repo.get_by_clerk_user_id()
    assert got2 is not None and got2.id == created.id

    updated = await repo.update(created.id, type("Obj", (), {
        "clerk_user_id": "test_user",
        "access_token": "a2",
        "token_type": "bearer",
        "expires_in": 7200,
        "refresh_token": "r2",
        "scope": "*",
        "expires_at": datetime.utcnow() + timedelta(hours=2),
    })())
    assert updated.access_token == "a2"

    res = await repo.delete(created.id)
    assert res["message"] == "SoundcloudToken deleted successfully"


