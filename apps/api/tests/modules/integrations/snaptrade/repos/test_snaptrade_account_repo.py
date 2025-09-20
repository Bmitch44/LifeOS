import pytest

from app.modules.integrations.snaptrade.repos.account_repo import SnaptradeAccountRepo
from tests.factories.integrations.snaptrade import create_snaptrade_account


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    for i in range(3):
        await create_snaptrade_account(session, account_id=f"sacc_{i}")
    for i in range(2):
        await create_snaptrade_account(session, clerk_user_id="other", account_id=f"o_sacc_{i}")

    repo = SnaptradeAccountRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(1, 10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(a.clerk_user_id == "test_user" for a in page.items)


@pytest.mark.anyio
async def test_create_get_get_by_account_id(session):
    repo = SnaptradeAccountRepo(session, clerk_user_id="test_user")
    created = await repo.create(
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "account_id": "s1",
            "connection_id": "c1",
            "name": "Name",
            "number": "0001",
            "institution_name": "Inst",
            "status": "active",
            "type": "cash",
            "current_balance": 10.0,
            "currency": "USD",
        })()
    )
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id
    got2 = await repo.get_by_account_id("s1")
    assert got2 is not None and got2.id == created.id


@pytest.mark.anyio
async def test_update(session):
    acc = await create_snaptrade_account(session, name="Old", current_balance=1.0)
    repo = SnaptradeAccountRepo(session, clerk_user_id="test_user")
    updated = await repo.update(
        acc.id,
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "account_id": acc.account_id,
            "connection_id": acc.connection_id,
            "name": "New",
            "number": "9999",
            "institution_name": "Inst",
            "status": "inactive",
            "type": "cash",
            "current_balance": 2.0,
            "currency": "USD",
        })()
    )
    assert updated.name == "New"
    assert updated.current_balance == 2.0


@pytest.mark.anyio
async def test_delete(session):
    acc = await create_snaptrade_account(session)
    repo = SnaptradeAccountRepo(session, clerk_user_id="test_user")
    res = await repo.delete(acc.id)
    assert res["message"] == "Account deleted successfully"


