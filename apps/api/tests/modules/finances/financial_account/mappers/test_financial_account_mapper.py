import pytest

# Placeholder: Financial accounts are mapped from integrations; test the two mappers
from app.modules.integrations.plaid.mappers.plaid_account_mapper import PlaidAccountToFinancialAccountMapper
from app.modules.integrations.snaptrade.mappers.snaptrade_account_mapper import SnaptradeAccountMapper
from app.db.models import PlaidAccount, SnaptradeAccount


@pytest.mark.anyio
async def test_plaid_to_financial_account_mapper_basic():
    mapper = PlaidAccountToFinancialAccountMapper("test_user")
    acc = PlaidAccount(
        clerk_user_id="test_user",
        account_id="acc1",
        name="Name",
        official_name="Off",
        type="depository",
        subtype="checking",
        current_balance=10.0,
        available_balance=9.0,
        iso_currency_code="USD",
        mask="1234",
    )
    fa = mapper.map_plaid_account_to_financial_account(acc)
    assert fa.clerk_user_id == "test_user"
    assert fa.source == "plaid"
    assert fa.source_account_id == "acc1"
    assert fa.current_balance == 10.0


@pytest.mark.anyio
async def test_snaptrade_to_financial_account_mapper_basic():
    mapper = SnaptradeAccountMapper("test_user")
    acc = SnaptradeAccount(
        clerk_user_id="test_user",
        account_id="s1",
        connection_id="c1",
        name="Name",
        number="0001",
        institution_name="Inst",
        status="active",
        type="cash",
        current_balance=100.0,
        currency="USD",
    )
    fa = mapper.map_snaptrade_account_to_financial_account(acc)
    assert fa.clerk_user_id == "test_user"
    assert fa.source == "snaptrade"
    assert fa.source_account_id == "s1"
    assert fa.current_balance == 100.0


