from app.modules.integrations.plaid.models import PlaidAccount
from app.modules.finances.schemas import FinancialAccountCreate
from app.modules.integrations.plaid.schemas import PlaidAccountCreate
from plaid.model.account_base import AccountBase
from pydantic import ValidationError

class PlaidAccountToFinancialAccountMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_plaid_account_to_financial_account(self, plaid_account: PlaidAccount) -> FinancialAccountCreate:
        try:
            financial_account = FinancialAccountCreate(
                clerk_user_id=plaid_account.clerk_user_id,
                type=plaid_account.type,
                name=plaid_account.name,
                institution_name=plaid_account.official_name,
                currency=plaid_account.iso_currency_code,
                current_balance=plaid_account.current_balance,
                source="plaid",
                source_account_id=plaid_account.account_id,
            )
            return financial_account
        except Exception as e:
            raise ValidationError(status_code=500, detail=f"Failed to map plaid account to financial account: {e}") from e

    def map_api_account_to_plaid_account(self, api_account: AccountBase) -> PlaidAccountCreate:
        try:
            balances = getattr(api_account, "balances", None)
            plaid_account = PlaidAccountCreate(
                clerk_user_id=self.clerk_user_id,
                account_id=api_account.get("account_id"),
                name=api_account.get("name"),
                official_name=api_account.get("official_name"),
                type=api_account.get("type"),
                subtype=api_account.get("subtype"),
                current_balance=getattr(balances, "current", None) if balances else None,
                available_balance=getattr(balances, "available", None) if balances else None,
                iso_currency_code=getattr(balances, "iso_currency_code", None) if balances else None,
                mask=api_account.get("mask"),
            )
            return plaid_account
        except Exception as e:
            raise ValidationError(status_code=500, detail=f"Failed to map api account to plaid account: {e}") from e