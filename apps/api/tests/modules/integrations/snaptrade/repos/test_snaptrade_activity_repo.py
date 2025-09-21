import pytest

from app.modules.integrations.snaptrade.repos.activity_repo import SnaptradeActivityRepo
from tests.factories.integrations.snaptrade import create_snaptrade_activity


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    for i in range(3):
        await create_snaptrade_activity(session, activity_id=f"a_{i}")
    for i in range(2):
        await create_snaptrade_activity(session, clerk_user_id="other", activity_id=f"o_{i}")

    repo = SnaptradeActivityRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(1, 10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(a.clerk_user_id == "test_user" for a in page.items)


@pytest.mark.anyio
async def test_get_and_get_by_activity_id(session):
    act = await create_snaptrade_activity(session, activity_id="a_1")
    repo = SnaptradeActivityRepo(session, clerk_user_id="test_user")
    got = await repo.get(act.id)
    assert got.id == act.id
    got2 = await repo.get_by_activity_id("a_1")
    assert got2 is not None and got2.id == act.id


@pytest.mark.anyio
async def test_delete(session):
    act = await create_snaptrade_activity(session)
    repo = SnaptradeActivityRepo(session, clerk_user_id="test_user")
    res = await repo.delete(act.id)
    assert res["message"] == "Activity deleted successfully"


