from pydantic import ValidationError
from app.modules.integrations.snaptrade.schemas import SnaptradeActivityCreate
from snaptrade_client.type.paginated_universal_activity import AccountUniversalActivity

class SnaptradeActivityMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_api_account_to_snaptrade_account(self, api_activity: AccountUniversalActivity, account_id: int) -> SnaptradeActivityCreate:
        try:
            symbol = api_activity.get("symbol")
            option_symbol = api_activity.get("option_symbol")
            currency = api_activity.get("currency")
            return SnaptradeActivityCreate(
                clerk_user_id=self.clerk_user_id,
                account_id=account_id,
                activity_id=api_activity.get("id"),
                symbol_id=symbol.get("id") if symbol else None,
                option_symbol_id=option_symbol.get("id") if option_symbol else None,
                type=api_activity.get("type"),
                option_type=api_activity.get("option_type"),
                price=api_activity.get("price") or None,
                units=api_activity.get("units") or None,
                amount=api_activity.get("amount"),
                description=api_activity.get("description") or None,
                trade_date=api_activity.get("trade_date"),
                settlement_date=api_activity.get("settlement_date") or None,
                currency=currency.get("code") if currency else "CAD",
                fees=api_activity.get("fee") or None,
                fx_rate=api_activity.get("fx_rate"),
                institution=api_activity.get("institution") or None,
            )
        except Exception as e:
            raise ValidationError(f"Failed to map snaptrade activity: {e}") from e
