import pytest

from tests.factories.integrations.plaid import create_plaid_item


@pytest.mark.anyio
async def test_list_items(client, session):
    for i in range(5):
        await create_plaid_item(session, item_id=f"item_{i}", access_token=f"token_{i}")

    r = await client.get("/v1/plaid/items", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_item(client, session):
    item = await create_plaid_item(session)
    r = await client.get(f"/v1/plaid/items/{item.id}")
    assert r.status_code == 200
    assert r.json()["id"] == item.id


@pytest.mark.anyio
async def test_create_item(client):
    payload = {
        "clerk_user_id": "test_user",
        "item_id": "item_new",
        "access_token": "token_new",
        "institution_name": "Inst",
    }
    r = await client.post("/v1/plaid/items", json=payload)
    assert r.status_code == 201
    assert r.json()["item_id"] == "item_new"


@pytest.mark.anyio
async def test_update_item(client, session):
    item = await create_plaid_item(session)
    payload = {
        "clerk_user_id": "test_user",
        "item_id": item.item_id,
        "access_token": "token_updated",
        "institution_name": "NewInst",
    }
    r = await client.put(f"/v1/plaid/items/{item.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["access_token"] == "token_updated"


@pytest.mark.anyio
async def test_delete_item(client, session):
    item = await create_plaid_item(session)
    r = await client.delete(f"/v1/plaid/items/{item.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Item deleted successfully"


@pytest.mark.anyio
async def test_sync_items_no_items(client):
    r = await client.get("/v1/plaid/items/sync")
    assert r.status_code == 200
    assert r.json()["message"] in {"No items to sync", "Items synced successfully"}


