import json
import pytest
from sqlalchemy import select

from app.modules.integrations.plaid.services import PlaidAccountService
from tests._shared.factories.plaid import create_plaid_item


@pytest.mark.integration
async def test_plaid_sync_creates_accounts(db_session, mock_plaid):
    await create_plaid_item(db_session, access_token="acc_123", clerk_user_id="user_test")

    accounts = json.loads(open("apps/api/tests/_shared/data/plaid/accounts.json").read())
    mock_plaid(
        accounts=accounts,
        item=json.loads(open("apps/api/tests/_shared/data/plaid/item.json").read()),
        exchange={"access_token": "acc_123", "item_id": "it_123"},
    )

    svc = PlaidAccountService(db_session)
    res = await svc.sync_accounts("user_test")
    assert res["message"].startswith("Accounts synced")

    from app.db.models import PlaidAccount

    pa = (await db_session.execute(select(PlaidAccount))).scalars().all()
    assert len(pa) == 1