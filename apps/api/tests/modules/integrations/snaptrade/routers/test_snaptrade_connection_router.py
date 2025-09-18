import pytest

from tests.factories.integrations.snaptrade import create_snaptrade_connection


@pytest.mark.anyio
async def test_list_connections(client, session):
    for i in range(5):
        await create_snaptrade_connection(session, connection_id=f"conn_{i}")

    r = await client.get("/v1/snaptrade/connections", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_connection(client, session):
    conn = await create_snaptrade_connection(session)
    r = await client.get(f"/v1/snaptrade/connections/{conn.id}")
    assert r.status_code == 200
    assert r.json()["id"] == conn.id


@pytest.mark.anyio
async def test_create_connection(client):
    payload = {
        "clerk_user_id": "test_user",
        "connection_id": "conn_new",
        "user_secret": "secret_new",
        "brokerage_name": "Broker",
    }
    r = await client.post("/v1/snaptrade/connections", json=payload)
    assert r.status_code == 201
    assert r.json()["connection_id"] == "conn_new"


@pytest.mark.anyio
async def test_update_connection(client, session):
    conn = await create_snaptrade_connection(session)
    payload = {
        "clerk_user_id": "test_user",
        "connection_id": "conn_updated",
        "user_secret": "secret_updated",
        "brokerage_name": "BrokerUpdated",
    }
    r = await client.put(f"/v1/snaptrade/connections/{conn.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["connection_id"] == "conn_updated"


@pytest.mark.anyio
async def test_delete_connection(client, session):
    conn = await create_snaptrade_connection(session)
    r = await client.delete(f"/v1/snaptrade/connections/{conn.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Connection deleted successfully"


@pytest.mark.anyio
async def test_sync_connections_no_connections(client):
    r = await client.get("/v1/snaptrade/connections/sync")
    assert r.status_code == 200
    assert r.json()["message"] in {"No connections to sync", "Connections synced successfully"}
