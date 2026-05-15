from functools import lru_cache
from pathlib import Path
from typing import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict

IS_MAIN = any("main.py" in child.name for child in Path.cwd().iterdir())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # Database
    DATABASE_URL: str = "sqlite:///:memory:"

    # JWT
    JWT_SECRET_KEY: str = "just-a-long-secret-key-for-json-web-token-123123"
    JWT_ACCESS_TOKEN_DUR: int = 5 * 60
    JWT_REFRESH_TOKEN_DUR: int = 7 * 3600
    AUTH_COOKIE_SECURE: bool = True

    # Languages
    LANGUAGES_LOCALES_DIR: str | Path = (
        "./src/locales" if IS_MAIN else "./locales"
    )
    SUPPORTED_LANGUAGES: Sequence[str] = ["fa", "en"]
    DEFAULT_LANGUAGE: str = "en"

    # Redis
    REDIS_URL: str = ""


@lru_cache
def get_settings():
    return Settings()
