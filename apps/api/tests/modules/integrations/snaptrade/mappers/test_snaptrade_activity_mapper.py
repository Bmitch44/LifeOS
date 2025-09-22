import pytest

from app.modules.integrations.snaptrade.mappers.snaptrade_activity_mapper import SnaptradeActivityMapper


class FakeApiActivity(dict):
    pass


@pytest.mark.anyio
async def test_map_api_activity_to_snaptrade_activity_full():
    mapper = SnaptradeActivityMapper("test_user")
    api = FakeApiActivity(
        id="a1",
        symbol={"id": "sym1"},
        option_symbol={"id": "opt1"},
        type="trade",
        option_type="call",
        price=10.5,
        units=2,
        amount=21.0,
        description="Buy",
        trade_date="2024-01-01T00:00:00Z",
        settlement_date="2024-01-03T00:00:00Z",
        currency={"code": "USD"},
        fee=0.1,
        fx_rate=1.0,
        institution="Broker",
    )
    p = mapper.map_api_activity_to_snaptrade_activity(api, account_id=1)

    assert p.clerk_user_id == "test_user"
    assert p.account_id == 1
    assert p.activity_id == "a1"
    assert p.symbol_id == "sym1"
    assert p.option_symbol_id == "opt1"
    assert p.type == "trade"
    assert p.option_type == "call"
    assert p.price == 10.5
    assert p.units == 2
    assert p.amount == 21.0
    assert p.description == "Buy"
    assert p.currency == "USD"
    assert p.fees == 0.1
    assert p.fx_rate == 1.0
    assert p.institution == "Broker"


@pytest.mark.anyio
async def test_map_api_activity_to_snaptrade_activity_defaults():
    mapper = SnaptradeActivityMapper("test_user")
    api = FakeApiActivity(id="a2")
    p = mapper.map_api_activity_to_snaptrade_activity(api, account_id=1)

    assert p.clerk_user_id == "test_user"
    assert p.account_id == 1
    assert p.activity_id == "a2"
    assert p.symbol_id is None
    assert p.option_symbol_id is None
    assert p.currency == "CAD"  # default


