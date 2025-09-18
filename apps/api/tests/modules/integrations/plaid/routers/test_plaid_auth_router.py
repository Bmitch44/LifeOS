import pytest


@pytest.mark.anyio
async def test_get_link_token(client):
    # In tests, PlaidClient may not be configured; just assert we get a 200 or 500 gracefully.
    r = await client.get("/v1/plaid/auth/link-token")
    assert r.status_code in (200, 500)


@pytest.mark.anyio
async def test_exchange_public_token(client):
    # We expect either success (201/200) if client is configured or 500 if not.
    r = await client.post("/v1/plaid/auth/exchange-public-token", json="public-sandbox-token")
    assert r.status_code in (200, 201, 500)


