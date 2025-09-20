import pytest

from app.modules.integrations.snaptrade.repos.connection_repo import SnaptradeConnectionRepo
from tests.factories.integrations.snaptrade import create_snaptrade_connection


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    for i in range(3):
        await create_snaptrade_connection(session, connection_id=f"conn_{i}")
    for i in range(2):
        await create_snaptrade_connection(session, clerk_user_id="other", connection_id=f"o_conn_{i}")

    repo = SnaptradeConnectionRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(1, 10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(c.clerk_user_id == "test_user" for c in page.items)


@pytest.mark.anyio
async def test_create_get_get_by_connection_id_and_by_user(session):
    repo = SnaptradeConnectionRepo(session, clerk_user_id="test_user")
    created = await repo.create(
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "user_secret": "sec_1",
            "connection_id": "cid_1",
            "brokerage_name": "Broker",
        })()
    )
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id
    got2 = await repo.get_by_connection_id("cid_1")
    assert got2 is not None and got2.id == created.id
    got3 = await repo.get_by_clerk_user_id()
    assert got3 is not None and got3.id == created.id


@pytest.mark.anyio
async def test_update(session):
    conn = await create_snaptrade_connection(session, brokerage_name="Old")
    repo = SnaptradeConnectionRepo(session, clerk_user_id="test_user")
    updated = await repo.update(
        conn.id,
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "user_secret": conn.user_secret,
            "connection_id": conn.connection_id,
            "brokerage_name": "NewBroker",
        })()
    )
    assert updated.brokerage_name == "NewBroker"


@pytest.mark.anyio
async def test_delete(session):
    conn = await create_snaptrade_connection(session)
    repo = SnaptradeConnectionRepo(session, clerk_user_id="test_user")
    res = await repo.delete(conn.id)
    assert res["message"] == "Connection deleted successfully"


