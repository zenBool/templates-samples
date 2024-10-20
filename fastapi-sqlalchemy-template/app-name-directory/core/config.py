import os
from typing import Optional

from pydantic import BaseModel, model_validator
from pydantic import PostgresDsn

from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8080


class APIV1Prefix(BaseModel):
    prefix: str = "/v1"
    tag: str = "API_v1"
    users: str = "/users"


class APIPrefix(BaseModel):
    prefix: str = "/api"
    tag: str = "API"
    v1: APIV1Prefix = APIV1Prefix()


class DBConfig(BaseModel):
    # host: str = os.getenv("DB_HOST", "192.168.3.50")
    # port: int = os.getenv("DB_PORT", 5432)
    # user: str = os.getenv("DB_USER", "postgres")
    # password: str = os.getenv("DB_PASSWORD", "")
    # database: str = os.getenv("DB_DATABASE", "fastalchemy")

    url: Optional[PostgresDsn] = None  # "postgresql+asyncpg://user:pass@host/dbname"

    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 45
    pool_size: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("template.env", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FAPI_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    db: DBConfig = DBConfig()


settings = Settings()
print(settings.db.echo)
print(settings.db.url)
