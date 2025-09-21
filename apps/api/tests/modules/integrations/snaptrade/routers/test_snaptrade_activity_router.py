import pytest

from tests.factories.integrations.snaptrade import create_snaptrade_activity


@pytest.mark.anyio
async def test_list_activities(client, session):
    for i in range(5):
        await create_snaptrade_activity(session, activity_id=f"a_{i}")

    r = await client.get("/v1/snaptrade/activities", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_activity(client, session):
    act = await create_snaptrade_activity(session)
    r = await client.get(f"/v1/snaptrade/activities/{act.id}")
    assert r.status_code == 200
    assert r.json()["id"] == act.id


@pytest.mark.anyio
async def test_create_activity(client):
    payload = {
        "clerk_user_id": "test_user",
        "activity_id": "a_new",
        "account_id": 1,
        "symbol_id": "sym_1",
        "option_symbol_id": "opt_1",
        "type": "trade",
        "option_type": "call",
        "price": 10.0,
        "units": 1.0,
        "amount": 10.0,
        "description": "Buy",
        "trade_date": "2024-01-01T00:00:00Z",
        "settlement_date": "2024-01-01T00:00:00Z",
        "currency": "USD",
        "fees": 0.0,
        "fx_rate": 1.0,
        "institution": "Test",
    }
    r = await client.post("/v1/snaptrade/activities", json=payload)
    assert r.status_code == 201
    assert r.json()["activity_id"] == "a_new"


@pytest.mark.anyio
async def test_update_activity(client, session):
    act = await create_snaptrade_activity(session)
    payload = {
        "clerk_user_id": "test_user",
        "activity_id": act.activity_id,
        "account_id": act.account_id,
        "symbol_id": "sym_2",
        "option_symbol_id": "opt_2",
        "type": "trade",
        "option_type": "call",
        "price": 20.0,
        "units": 2.0,
        "amount": 40.0,
        "description": "Update",
        "trade_date": "2024-01-02T00:00:00Z",
        "settlement_date": "2024-01-02T00:00:00Z",
        "currency": "USD",
        "fees": 0.5,
        "fx_rate": 1.0,
        "institution": "Test",
    }
    r = await client.put(f"/v1/snaptrade/activities/{act.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["amount"] in (None, 40.0)


@pytest.mark.anyio
async def test_delete_activity(client, session):
    act = await create_snaptrade_activity(session)
    r = await client.delete(f"/v1/snaptrade/activities/{act.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Activity deleted successfully"


@pytest.mark.anyio
async def test_sync_activities_no_connections(client):
    r = await client.get("/v1/snaptrade/activities/sync/1")
    assert r.status_code == 200
    assert r.json()["message"] in {"No connections to sync", "Activities synced successfully"}


