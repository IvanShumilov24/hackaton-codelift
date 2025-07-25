from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TG_TOKEN: str
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
