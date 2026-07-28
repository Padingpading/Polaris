"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Polaris Admin"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 120
    database_url: str = (
        "mysql+pymysql://user:password@127.0.0.1:3306/polaris?charset=utf8mb4"
    )
    cors_origins: List[str] = ["http://localhost:5173"]
    api_prefix: str = "/api/v1"
    algorithm: str = "HS256"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
