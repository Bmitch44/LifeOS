import pytest

from tests.factories.integrations.plaid import create_plaid_account


@pytest.mark.anyio
async def test_list_accounts(client, session):
    for i in range(5):
        await create_plaid_account(session, account_id=f"acc_{i}")

    r = await client.get("/v1/plaid/accounts", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_account(client, session):
    acc = await create_plaid_account(session)
    r = await client.get(f"/v1/plaid/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["id"] == acc.id


@pytest.mark.anyio
async def test_create_account(client):
    payload = {
        "clerk_user_id": "test_user",
        "account_id": "acc_new",
        "name": "Name",
        "official_name": "Official",
        "type": "depository",
        "subtype": "checking",
        "current_balance": 10.0,
        "available_balance": 5.0,
        "iso_currency_code": "USD",
        "mask": "4321",
    }
    r = await client.post("/v1/plaid/accounts", json=payload)
    assert r.status_code == 201
    assert r.json()["account_id"] == "acc_new"


@pytest.mark.anyio
async def test_update_account(client, session):
    acc = await create_plaid_account(session)
    payload = {
        "clerk_user_id": "test_user",
        "account_id": acc.account_id,
        "name": "New",
        "official_name": "New",
        "type": "depository",
        "subtype": "savings",
        "current_balance": 200.0,
        "available_balance": 150.0,
        "iso_currency_code": "USD",
        "mask": "9999",
    }
    r = await client.put(f"/v1/plaid/accounts/{acc.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["subtype"] == "savings"


@pytest.mark.anyio
async def test_delete_account(client, session):
    acc = await create_plaid_account(session)
    r = await client.delete(f"/v1/plaid/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Account deleted successfully"


@pytest.mark.anyio
async def test_sync_accounts_no_items(client):
    r = await client.get("/v1/plaid/accounts/sync")
    assert r.status_code == 200
    assert r.json()["message"] in {"No items to sync", "Accounts synced successfully"}


