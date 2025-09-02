from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class PgUserSettings(BaseModel):
    user_db_dsn: str = "postgresql+asyncpg://developer:password@localhost:5433/users_db"


class RabbitSettings(BaseModel):
    rabbitmq_url: str = "amqp://developer:password@localhost:5672/"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env",),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DEBUG: bool = False
    SQL_ECHO: bool = False

    rabbit: RabbitSettings = Field(default_factory=RabbitSettings)
    user_pg: PgUserSettings = Field(default_factory=PgUserSettings)


settings = AppSettings()
