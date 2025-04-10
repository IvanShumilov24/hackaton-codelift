from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TG_TOKEN: str
    DB_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")
