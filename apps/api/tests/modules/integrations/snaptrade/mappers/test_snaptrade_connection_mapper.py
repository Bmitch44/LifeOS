import pytest

from app.modules.integrations.snaptrade.mappers.snaptrade_connection_mapper import SnaptradeConnectionMapper


class FakeApiConnection(dict):
    pass


@pytest.mark.anyio
async def test_map_api_connection_to_snaptrade_connection_minimal():
    mapper = SnaptradeConnectionMapper("test_user")
    api_conn = FakeApiConnection(id="conn_1", brokerage={"name": "Snap Brokerage"})
    payload = mapper.map_api_connection_to_snaptrade_connection(api_conn, user_secret="usec")

    assert payload.clerk_user_id == "test_user"
    assert payload.connection_id == "conn_1"
    assert payload.user_secret == "usec"
    assert payload.brokerage_name == "Snap Brokerage"


@pytest.mark.anyio
async def test_map_api_connection_to_snaptrade_connection_missing_brokerage():
    mapper = SnaptradeConnectionMapper("test_user")
    api_conn = FakeApiConnection(id="conn_2")
    payload = mapper.map_api_connection_to_snaptrade_connection(api_conn, user_secret="usec")

    assert payload.clerk_user_id == "test_user"
    assert payload.connection_id == "conn_2"
    assert payload.user_secret == "usec"
    assert payload.brokerage_name is None


