from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from datetime import timedelta

class Settings(BaseSettings):
    secret_api: str
    postgres_dsn: PostgresDsn
    db_user: str
    db_pass: str
    db_name: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    refresh_token_expire: timedelta = timedelta(days=30)
	access_token_expire: timedelta = timedelta(minutes=15)


settings = Settings()
