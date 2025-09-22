import pytest

from app.modules.integrations.snaptrade.mappers.snaptrade_account_mapper import SnaptradeAccountMapper
from app.db.models import SnaptradeAccount


class FakeApiAccount(dict):
    pass


@pytest.mark.anyio
async def test_map_snaptrade_account_to_financial_account():
    mapper = SnaptradeAccountMapper("test_user")
    s = SnaptradeAccount(
        clerk_user_id="test_user",
        snaptrade_account_id="s1",
        connection_id=1,
        name="Name",
        number="0001",
        institution_name="Inst",
        status="active",
        type="cash",
        current_balance=100.0,
        currency="USD",
    )
    fa = mapper.map_snaptrade_account_to_financial_account(s)
    assert fa.clerk_user_id == "test_user"
    assert fa.source == "snaptrade"
    assert fa.source_account_id == "s1"
    assert fa.current_balance == 100.0
    assert fa.currency == "USD"


@pytest.mark.anyio
async def test_map_api_account_to_snaptrade_account_with_balance():
    mapper = SnaptradeAccountMapper("test_user")
    api_acc = FakeApiAccount(
        id="s1",
        brokerage_authorization=1,
        name="Ext",
        number="9999",
        institution_name="Inst",
        status="active",
        raw_type="cash",
        balance={"total": {"amount": 12.3, "currency": "USD"}},
    )
    p = mapper.map_api_account_to_snaptrade_account(api_acc)
    assert p.clerk_user_id == "test_user"
    assert p.snaptrade_account_id == "s1"
    assert p.connection_id == 1
    assert p.current_balance == 12.3
    assert p.currency == "USD"


@pytest.mark.anyio
async def test_map_api_account_to_snaptrade_account_without_balance_defaults():
    mapper = SnaptradeAccountMapper("test_user")
    api_acc = FakeApiAccount(
        id="s1",
        brokerage_authorization=1,
        name="Ext",
        number="9999",
        institution_name="Inst",
        status="active",
        raw_type="cash",
    )
    p = mapper.map_api_account_to_snaptrade_account(api_acc)
    assert p.current_balance == 0
    assert p.currency == "CAD"


