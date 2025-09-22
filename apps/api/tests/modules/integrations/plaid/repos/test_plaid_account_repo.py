import pytest

from app.modules.integrations.plaid.repos.account_repo import PlaidAccountRepo
from tests.factories.integrations.plaid import create_plaid_account


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    for i in range(3):
        await create_plaid_account(session, plaid_account_id=f"acc_{i}")
    for i in range(2):
        await create_plaid_account(session, clerk_user_id="other", plaid_account_id=f"o_acc_{i}")

    repo = PlaidAccountRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(1, 10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(a.clerk_user_id == "test_user" for a in page.items)


@pytest.mark.anyio
async def test_create_get_get_by_account_id(session):
    repo = PlaidAccountRepo(session, clerk_user_id="test_user")
    created = await repo.create(
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "plaid_account_id": "acc1",
            "name": "Name",
            "official_name": "Official",
            "type": "depository",
            "subtype": "checking",
            "current_balance": 10.0,
            "available_balance": 9.0,
            "iso_currency_code": "USD",
            "mask": "1234",
        })()
    )
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id
    got2 = await repo.get_by_account_id("acc1")
    assert got2 is not None and got2.id == created.id


@pytest.mark.anyio
async def test_update(session):
    acc = await create_plaid_account(session, name="Old")
    repo = PlaidAccountRepo(session, clerk_user_id="test_user")
    updated = await repo.update(
        acc.id,
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "plaid_account_id": acc.plaid_account_id,
            "name": "New",
            "official_name": "Official",
            "type": "depository",
            "subtype": "checking",
            "current_balance": 11.0,
            "available_balance": 9.0,
            "iso_currency_code": "USD",
            "mask": "1234",
        })()
    )
    assert updated.name == "New"
    assert updated.current_balance == 11.0


@pytest.mark.anyio
async def test_delete(session):
    acc = await create_plaid_account(session)
    repo = PlaidAccountRepo(session, clerk_user_id="test_user")
    res = await repo.delete(acc.id)
    assert res["message"] == "Account deleted successfully"


