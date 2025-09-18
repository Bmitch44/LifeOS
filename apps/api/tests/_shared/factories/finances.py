from app.db.models import FinancialAccount


async def create_financial_account(session, **overrides):
    fa = FinancialAccount(
        clerk_user_id=overrides.get("clerk_user_id", "user_test"),
        type=overrides.get("type", "bank"),
        name=overrides.get("name", "My Account"),
        institution_name=overrides.get("institution_name", "Test Bank"),
        currency=overrides.get("currency", "CAD"),
        current_balance=overrides.get("current_balance", 100.0),
        source=overrides.get("source", "plaid"),
        source_account_id=overrides.get("source_account_id", "src_123"),
    )
    session.add(fa)
    await session.commit()
    await session.refresh(fa)
    return fa