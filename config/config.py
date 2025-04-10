from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TG_TOKEN: str
    DB_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"

    class Config:
        env_file = "../.env"