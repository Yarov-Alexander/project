from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:********@localhost:5432/postgres"
    secret_key: str
    algorithm: str = "HS256"
    refresh_token_expire_days: int = 7

    access_token_expire_minutes: int = 60
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
settings = Settings()