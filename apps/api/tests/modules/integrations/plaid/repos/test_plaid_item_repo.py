import pytest

from app.modules.integrations.plaid.repos.item_repo import PlaidItemRepo
from tests.factories.integrations.plaid import create_plaid_item


@pytest.mark.anyio
async def test_paginate_scoped_by_user(session):
    # Seed for test_user
    for i in range(3):
        await create_plaid_item(session, item_id=f"item_{i}", access_token=f"tok_{i}")
    # Seed for another user
    for i in range(2):
        await create_plaid_item(session, clerk_user_id="other", item_id=f"o_item_{i}", access_token=f"o_tok_{i}")

    repo = PlaidItemRepo(session, clerk_user_id="test_user")
    page = await repo.paginate(page=1, size=10)
    assert page.total == 3
    assert len(page.items) == 3
    assert all(item.clerk_user_id == "test_user" for item in page.items)


@pytest.mark.anyio
async def test_create_and_get(session):
    repo = PlaidItemRepo(session, clerk_user_id="test_user")
    created = await repo.create(
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "item_id": "iid_1",
            "access_token": "atok_1",
            "institution_name": "Inst",
        })()
    )
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id
    assert got.clerk_user_id == "test_user"


@pytest.mark.anyio
async def test_update(session):
    item = await create_plaid_item(session, institution_name="Old", access_token="t1")
    repo = PlaidItemRepo(session, clerk_user_id="test_user")
    updated = await repo.update(
        item.id,
        payload=type("Obj", (), {
            "clerk_user_id": "test_user",
            "item_id": item.item_id,
            "access_token": "t2",
            "institution_name": "NewInst",
        })()
    )
    assert updated.access_token == "t2"
    assert updated.institution_name == "NewInst"


@pytest.mark.anyio
async def test_delete(session):
    item = await create_plaid_item(session)
    repo = PlaidItemRepo(session, clerk_user_id="test_user")
    res = await repo.delete(item.id)
    assert res["message"] == "Item deleted successfully"


