from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str = "LifeOS API"
    api_version: str = "0.1.0"
    cors_origins: list[str] = ["*"]
    clerk_jwks_url: str | None = None
    clerk_issuer: str | None = None
    database_url: str | None = None
    snaptrade_consumer_key: str | None = None
    snaptrade_client_id: str | None = None
    snaptrade_custom_redirect_url: str | None = "http://localhost:3000/"
    plaid_client_id: str | None = None
    plaid_prod_secret: str | None = None
    plaid_sandbox_secret: str | None = None
    logfire_token: str | None = None

    model_config = {
        "env_file": ".env",
        "env_prefix": "LIFEOS_",
    }


settings = Settings()


