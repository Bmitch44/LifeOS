import pytest

from app.modules.finances.repos.financial_account_repo import FinancialAccountRepo
from tests.factories import create_financial_account


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    # Seed for test_user
    for i in range(3):
        await create_financial_account(session, source_account_id=f"u_src_{i}")
    # Seed for another user
    for i in range(2):
        await create_financial_account(session, clerk_user_id="other", source_account_id=f"o_src_{i}")

    repo = FinancialAccountRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(page=1, size=10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(item.clerk_user_id == "test_user" for item in page.items)


@pytest.mark.anyio
async def test_create_and_get(session):
    repo = FinancialAccountRepo(session, clerk_user_id="test_user")
    created = await repo.create(
        payload=
        # minimal payload
        type("Obj", (), {
            "clerk_user_id": "test_user",
            "type": "bank",
            "name": "Name",
            "institution_name": "Inst",
            "currency": "USD",
            "current_balance": 10.0,
            "source": "plaid",
            "source_account_id": "src_1",
        })()
    )
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id
    assert got.clerk_user_id == "test_user"


@pytest.mark.anyio
async def test_get_by_source_account_id(session):
    acc = await create_financial_account(session, source_account_id="src_abc")
    repo = FinancialAccountRepo(session, clerk_user_id="test_user")
    got = await repo.get_by_source_account_id("src_abc")
    assert got is not None
    assert got.id == acc.id


@pytest.mark.anyio
async def test_update(session):
    acc = await create_financial_account(session, name="Old", current_balance=1.0)
    repo = FinancialAccountRepo(session, clerk_user_id="test_user")
    updated = await repo.update(
        acc.id,
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "type": "bank",
            "name": "New",
            "institution_name": "Inst",
            "currency": "USD",
            "current_balance": 2.0,
            "source": acc.source,
            "source_account_id": acc.source_account_id,
        })()
    )
    assert updated.name == "New"
    assert updated.current_balance == 2.0


@pytest.mark.anyio
async def test_delete(session):
    acc = await create_financial_account(session)
    repo = FinancialAccountRepo(session, clerk_user_id="test_user")
    res = await repo.delete(acc.id)
    assert res["message"] == "Financial account deleted successfully"


