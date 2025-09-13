from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str = "LifeOS API"
    api_version: str = "0.1.0"
    cors_origins: list[str] = ["*"]
    clerk_jwks_url: str | None = None
    clerk_issuer: str | None = None

    model_config = {
        "env_file": ".env",
        "env_prefix": "LIFEOS_",
    }


settings = Settings()


