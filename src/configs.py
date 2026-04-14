from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "just-a-long-secret-key-for-json-web-token-123123"
    JWT_ACCESS_TOKEN_DUR: int = 5 * 60
    JWT_REFRESH_TOKEN_DUR: int = 7 * 3600

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
