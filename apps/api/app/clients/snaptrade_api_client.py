from fastapi import HTTPException
from typing import List
from app.settings import settings
from snaptrade_client import SnapTrade
from snaptrade_client.type.account import Account
from snaptrade_client.type.brokerage_authorization import BrokerageAuthorization


class SnaptradeClient:
    def __init__(self, clerk_user_id: str):
        self.clerk_user_id = clerk_user_id
        self.client = SnapTrade(
            consumer_key=settings.snaptrade_consumer_key,
            client_id=settings.snaptrade_client_id,
        )

    def create_connection_portal(self, snaptrade_user_secret: str) -> str:
        """
        Create a new connection portal and return the redirect URI
        """
        try:    
            response = self.client.authentication.login_snap_trade_user(
                user_id=str(self.clerk_user_id), 
                user_secret=str(snaptrade_user_secret),
                custom_redirect=settings.snaptrade_custom_redirect_url
            )
            if not response.body:
                raise HTTPException(status_code=500, detail=f"Failed to create connection portal: {response.body}")
            return response.body["redirectURI"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create connection portal: {e}") from e

    def register_user(self) -> dict:
        """
        Register a new user and return the user secret and user id
        """
        try:
            response = self.client.authentication.register_snap_trade_user(
                user_id=str(self.clerk_user_id),
            )
            if not response.body:
                raise HTTPException(status_code=500, detail=f"Failed to register user: {response.body}")
            return {"user_secret": response.body["userSecret"], "user_id": response.body["userId"]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to register user: {e}") from e

    def get_connections(self, snaptrade_user_secret: str) -> List[BrokerageAuthorization]:
        """Get all connections for a user"""
        try:
            response = self.client.connections.list_brokerage_authorizations(query_params={
                "userId": self.clerk_user_id,
                "userSecret": snaptrade_user_secret
            })
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Failed to get connections: {response.body}")
            return response.body
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get connections: {e}") from e

    def get_all_users(self) -> dict:
        """Get all users"""
        try:
            response = self.client.authentication.list_snap_trade_users()
            if not response.body:
                raise HTTPException(status_code=500, detail=f"Failed to get users: {response.body}")
            return response.body
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get users: {e}") from e

    def get_all_accounts(self, snaptrade_user_secret: str) -> List[Account]:
        """Get all accounts for a user"""
        try:
            response = self.client.account_information.list_user_accounts(query_params={
                "userId":self.clerk_user_id,
                "userSecret":snaptrade_user_secret
            })
            if not response.body:
                raise HTTPException(status_code=500, detail=f"Failed to get accounts: {response.body}")
            return response.body
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get accounts: {e}") from e

    def delete_user(self, clerk_user_id: str) -> dict:
        """Delete a user"""
        try:
            response = self.client.authentication.delete_snap_trade_user(user_id=clerk_user_id)
            if response.status != 200:
                raise HTTPException(status_code=500, detail=f"Failed to delete user: {response.body}")
            return response.body
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}") from e