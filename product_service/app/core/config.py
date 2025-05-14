from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Product Service")
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings() 