"""Snaptrade account router tests."""
import pytest

from tests.factories.integrations.snaptrade import create_snaptrade_account


@pytest.mark.anyio
async def test_list_accounts(client, session):
    for i in range(5):
        await create_snaptrade_account(session, snaptrade_account_id=f"s_{i}")

    r = await client.get("/v1/snaptrade/accounts", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_account(client, session):
    acc = await create_snaptrade_account(session)
    r = await client.get(f"/v1/snaptrade/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["id"] == acc.id


@pytest.mark.anyio
async def test_create_account(client):
    payload = {
        "clerk_user_id": "test_user",
        "snaptrade_account_id": "s1",
        "connection_id": 1,
        "name": "Name",
        "number": "1234",
        "institution_name": "Inst",
        "status": "active",
        "type": "cash",
        "current_balance": 100.0,
        "currency": "USD",
    }
    r = await client.post("/v1/snaptrade/accounts", json=payload)
    assert r.status_code == 201
    assert r.json()["snaptrade_account_id"] == "s1"


@pytest.mark.anyio
async def test_update_account(client, session):
    acc = await create_snaptrade_account(session)
    payload = {
        "clerk_user_id": "test_user",
        "snaptrade_account_id": acc.snaptrade_account_id,
        "connection_id": acc.connection_id,
        "name": "New",
        "number": "9999",
        "institution_name": "NewInst",
        "status": "inactive",
        "type": "cash",
        "current_balance": 200.0,
        "currency": "USD",
    }
    r = await client.put(f"/v1/snaptrade/accounts/{acc.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["number"] == "9999"


@pytest.mark.anyio
async def test_delete_account(client, session):
    acc = await create_snaptrade_account(session)
    r = await client.delete(f"/v1/snaptrade/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Account deleted successfully"


@pytest.mark.anyio
async def test_sync_accounts_no_connections(client):
    r = await client.get("/v1/snaptrade/accounts/sync")
    assert r.status_code == 200
    assert r.json()["message"] in {"No connections to sync", "Accounts synced successfully"}
