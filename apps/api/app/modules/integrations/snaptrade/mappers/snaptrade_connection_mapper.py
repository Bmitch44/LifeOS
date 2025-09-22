from app.core.exceptions import MapperError
from snaptrade_client.type.brokerage_authorization import BrokerageAuthorization
from app.modules.integrations.snaptrade.schemas import SnaptradeConnectionCreate

class SnaptradeConnectionMapper:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id

    def map_api_connection_to_snaptrade_connection(self, api_connection: BrokerageAuthorization, user_secret: str) -> SnaptradeConnectionCreate:
        try:
            brokerage = api_connection.get("brokerage", {})
            return SnaptradeConnectionCreate(
                clerk_user_id=self.clerk_user_id,
                snaptrade_connection_id=api_connection.get("id"),
                user_secret=user_secret,
                brokerage_name=brokerage.get("name") if brokerage else None)
        except Exception as e:
            raise MapperError(source="api connection", target="snaptrade connection", e=e) from e