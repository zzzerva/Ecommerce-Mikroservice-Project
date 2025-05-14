from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator


class Settings(BaseSettings):
    # Project settings
    project_name: str = "User Service"
    version: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    postgres_server: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "12345"
    postgres_db: str = "user_service"
    postgres_port: int = 5432

    # JWT settings
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Database URL
    database_url: Optional[PostgresDsn] = None

    @field_validator("database_url", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> any:
        if isinstance(v, str):
            return v
        
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql",
            username=values["postgres_user"],
            password=values["postgres_password"],
            host=values["postgres_server"],
            port=values["postgres_port"],
            path=f"/{values['postgres_db']}"
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class TestSettings(Settings):
    # Override database settings for testing
    postgres_server: str = "localhost"
    postgres_user: str = "test"
    postgres_password: str = "test"
    postgres_db: str = "test_db"
    postgres_port: int = 5432

    # Override JWT settings for testing
    JWT_SECRET_KEY: str = "test-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env.test",
        env_file_encoding="utf-8",
        extra="ignore"
    )


import os

def get_settings():
    if os.getenv("TESTING"):
        return TestSettings()
    return Settings()
settings = get_settings()