import pytest

from tests.factories import create_financial_account


@pytest.mark.anyio
async def test_list_financial_accounts(client, session):
    for i in range(5):
        await create_financial_account(session, source_account_id=f"src_{i}")
    r = await client.get("/v1/finances/accounts", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_financial_account(client, session):
    acc = await create_financial_account(session)
    r = await client.get(f"/v1/finances/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["id"] == acc.id


@pytest.mark.anyio
async def test_create_financial_account(client):
    payload = {
        "clerk_user_id": "test_user",
        "type": "bank",
        "name": "New",
        "institution_name": "Inst",
        "currency": "USD",
        "current_balance": 50.0,
        "source": "plaid",
        "source_account_id": "src_new",
    }
    r = await client.post("/v1/finances/accounts", json=payload)
    assert r.status_code == 200
    assert r.json()["source_account_id"] == "src_new"


@pytest.mark.anyio
async def test_update_financial_account(client, session):
    acc = await create_financial_account(session)
    payload = {
        "clerk_user_id": "test_user",
        "type": "bank",
        "name": "Updated",
        "institution_name": "Inst",
        "currency": "USD",
        "current_balance": 60.0,
        "source": acc.source,
        "source_account_id": acc.source_account_id,
    }
    r = await client.put(f"/v1/finances/accounts/{acc.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"


@pytest.mark.anyio
async def test_delete_financial_account(client, session):
    acc = await create_financial_account(session)
    r = await client.delete(f"/v1/finances/accounts/{acc.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Financial account deleted successfully"
