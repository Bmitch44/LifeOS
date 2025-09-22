import pytest
from types import SimpleNamespace

from app.modules.integrations.plaid.mappers.plaid_account_mapper import PlaidAccountToFinancialAccountMapper
from app.db.models import PlaidAccount


class FakeBalances(SimpleNamespace):
    def __init__(self, current=None, available=None, iso_currency_code=None):
        super().__init__(current=current, available=available, iso_currency_code=iso_currency_code)


class FakeApiAccount(dict):
    def __init__(self, *, balances: FakeBalances | None = None, **kwargs):
        super().__init__(**kwargs)
        if balances is not None:
            self.balances = balances


@pytest.mark.anyio
async def test_map_plaid_account_to_financial_account():
    mapper = PlaidAccountToFinancialAccountMapper("test_user")
    p = PlaidAccount(
        clerk_user_id="test_user",
        plaid_account_id="acc1",
        name="Name",
        official_name="Official",
        type="depository",
        subtype="checking",
        current_balance=100.0,
        available_balance=90.0,
        iso_currency_code="USD",
        mask="1234",
    )
    fa = mapper.map_plaid_account_to_financial_account(p)
    assert fa.clerk_user_id == "test_user"
    assert fa.name == "Name"
    assert fa.institution_name == "Official"
    assert fa.type == "depository"
    assert fa.currency == "USD"
    assert fa.current_balance == 100.0
    assert fa.source == "plaid"
    assert fa.source_account_id == "acc1"


@pytest.mark.anyio
async def test_map_api_account_to_plaid_account_with_balances():
    mapper = PlaidAccountToFinancialAccountMapper("test_user")
    api_acc = FakeApiAccount(
        balances=FakeBalances(current=10.5, available=9.0, iso_currency_code="USD"),
        account_id="acc_ext",
        name="ExtName",
        official_name="ExtOfficial",
        type={"value": "depository"},
        subtype={"value": "checking"},
        mask="5678",
    )
    p = mapper.map_api_account_to_plaid_account(api_acc)
    assert p.clerk_user_id == "test_user"
    assert p.plaid_account_id == "acc_ext"
    assert p.name == "ExtName"
    assert p.official_name == "ExtOfficial"
    assert p.type == "depository"
    assert p.subtype == "checking"
    assert p.current_balance == 10.5
    assert p.available_balance == 9.0
    assert p.iso_currency_code == "USD"
    assert p.mask == "5678"


@pytest.mark.anyio
async def test_map_api_account_to_plaid_account_without_balances_defaults():
    mapper = PlaidAccountToFinancialAccountMapper("test_user")
    api_acc = FakeApiAccount(
        account_id="acc_ext",
        name="ExtName",
        official_name="ExtOfficial",
        type={"value": "investment"},
        subtype={"value": "brokerage"},
        mask="9999",
    )
    p = mapper.map_api_account_to_plaid_account(api_acc)
    assert p.current_balance is None
    assert p.available_balance is None
    # when balances missing, current implementation sets None
    assert p.iso_currency_code is None


