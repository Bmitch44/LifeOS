from app.db.models import PlaidItem, PlaidAccount


async def create_plaid_item(session, **overrides):
    item = PlaidItem(
        clerk_user_id=overrides.get("clerk_user_id", "user_test"),
        item_id=overrides.get("item_id", "it_123"),
        access_token=overrides.get("access_token", "acc_123"),
        institution_name=overrides.get("institution_name"),
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def create_plaid_account(session, **overrides):
    acct = PlaidAccount(
        clerk_user_id=overrides.get("clerk_user_id", "user_test"),
        account_id=overrides.get("account_id", "pa_123"),
        name=overrides.get("name", "Checking"),
        official_name=overrides.get("official_name", "Checking"),
        type=overrides.get("type", "depository"),
        subtype=overrides.get("subtype", "checking"),
        current_balance=overrides.get("current_balance", 100.0),
        available_balance=overrides.get("available_balance", 100.0),
        iso_currency_code=overrides.get("iso_currency_code", "CAD"),
        mask=overrides.get("mask", "1234"),
    )
    session.add(acct)
    await session.commit()
    await session.refresh(acct)
    return acct