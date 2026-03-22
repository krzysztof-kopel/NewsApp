from functools import lru_cache
import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NEWS_API_KEY: str
    DEEPL_API_KEY: str
    DEFAULT_PAGE_SIZE: int = 5
    ASYNC_CLIENT: httpx.AsyncClient = httpx.AsyncClient()
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_config():
    return Settings()
