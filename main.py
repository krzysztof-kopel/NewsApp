from functools import lru_cache
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NEWS_API_KEY: str
    DEFAULT_PAGE_SIZE: int = 5
    model_config = SettingsConfigDict(env_file=".env")

app = FastAPI()

@lru_cache
def get_config():
    return Settings()

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")
