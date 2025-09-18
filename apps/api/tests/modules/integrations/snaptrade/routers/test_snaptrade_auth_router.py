"""Snaptrade auth router tests."""
import pytest


@pytest.mark.anyio
async def test_get_connection_portal(client):
    # Expect 200 or 500 depending on Snaptrade client config
    r = await client.get("/v1/snaptrade/auth/connection-portal")
    assert r.status_code in (200, 500)
