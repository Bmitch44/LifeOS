import pytest

from app.modules.users.repo import UsersRepo
from tests.factories import create_user


@pytest.mark.anyio
async def test_paginate(session):
    for i in range(3):
        await create_user(session, clerk_user_id=f"u{i}", email=f"u{i}@ex.com")
    repo = UsersRepo(session)
    page = await repo.paginate(1, 2)
    assert page.total == 3
    assert page.page == 1
    assert page.size == 2
    assert len(page.items) == 2


@pytest.mark.anyio
async def test_get_update_delete(session):
    user = await create_user(session)
    repo = UsersRepo(session)
    got = await repo.get(user.id)
    assert got.id == user.id

    updated = await repo.update(user.id, type("Obj", (), {
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "Name",
        "phone": "123",
    })())
    assert updated.email == "new@example.com"

    res = await repo.delete(user.id)
    assert res["message"] == "User deleted successfully"


