from pydantic import ValidationError
from app.modules.finances.schemas import FinancialAccountCreate
from app.modules.integrations.snaptrade.models import SnaptradeAccount
from app.modules.integrations.snaptrade.schemas import SnaptradeAccountCreate
from snaptrade_client.type.account import Account

class SnaptradeAccountMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_snaptrade_account_to_financial_account(self, snaptrade_account: SnaptradeAccount) -> FinancialAccountCreate:
        try:
            return FinancialAccountCreate(
                clerk_user_id=snaptrade_account.clerk_user_id,
                type=snaptrade_account.type,
                name=snaptrade_account.name,
                institution_name=snaptrade_account.institution_name,
                currency=snaptrade_account.currency,
                current_balance=snaptrade_account.current_balance,
                source="snaptrade",
                source_account_id=snaptrade_account.account_id,
            )
        except Exception as e:
            raise ValidationError(status_code=500, detail=f"Failed to map snaptrade account to financial account: {e}") from e

    def map_api_account_to_snaptrade_account(self, api_account: Account) -> SnaptradeAccountCreate:
        try:
            balance_total = api_account.balance.get("total")
            return SnaptradeAccountCreate(
                clerk_user_id=self.clerk_user_id,
                account_id=api_account.id,
                connection_id=api_account.brokerage_authorization,
                name=api_account.name,  
                number=api_account.number,
                institution_name=api_account.institution_name,
                status=api_account.status,
                type=api_account.raw_type,
                current_balance=balance_total.get("amount") if balance_total else 0,
                currency=balance_total.get("currency") if balance_total else "CAD",
            )
        except Exception as e:
            raise ValidationError(status_code=500, detail=f"Failed to map api account to snaptrade account: {e}") from e
