from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from datetime import timedelta


class Settings(BaseSettings):
    dev_mode:bool
    postgres_dsn: str
    db_user: str
    db_pass: str
    db_name: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    refresh_token_expire: timedelta = timedelta(days=30)
    access_token_expire: timedelta = timedelta(minutes=15)
    secret_key: str


settings = Settings()
