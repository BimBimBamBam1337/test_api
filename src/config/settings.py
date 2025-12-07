from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pydantic import PostgresDsn
from datetime import timedelta


class Settings(BaseSettings):
    dev_mode: bool
    postgres_dsn: str
    db_user: str
    db_pass: str
    db_name: str
    refresh_token_expire: timedelta = timedelta(days=30)
    access_token_expire: timedelta = timedelta(days=7)
    secret_key: str
    algorithm: str = "sha256"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def logger_level(self) -> Literal["INFO", "DEBUG"]:
        if self.dev_mode:
            return "DEBUG"
        return "INFO"


settings = Settings()
