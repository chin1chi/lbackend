from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

DIR = Path(__file__).absolute().parent.parent
CORE_DIR = Path(__file__).absolute().parent
LOCALES_DIR = f'{CORE_DIR}/locales'
I18N_DOMAIN = 'messages'
PHOTO_PROOF_DIR = f'{DIR}/assets/photo-proof/'


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',extra="ignore")



class DBSettings(EnvBaseSettings):
    DB_HOST: str = 'db'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASS: str | None= None
    DB_NAME: str = 'lampa_db'

    @property
    def database_url(self) -> URL | str:
        if self.DB_PASS:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg2(self) -> str:
        if self.DB_PASS:
            return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CacheSettings(EnvBaseSettings):
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None= None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f'redis://{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0'
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0'


class AlembicSettings(EnvBaseSettings):
    DATABASE_URL_ALEMBIC: str | None = None
    ALEMBIC_CONFIG_PATH: str = str(Path(__file__).parent.parent / 'alembic.ini')

    @property
    def database_url_alembic(self) -> str:
        if not self.DATABASE_URL_ALEMBIC:
            raise ValueError("Alembic database URL is not set")
        return self.DATABASE_URL_ALEMBIC


class Settings(CacheSettings, DBSettings, AlembicSettings):
    DEBUG: bool = False
    AUTH_SECRET_KEY: str


settings = Settings()

print(settings.dict())  # Это выведет все загруженные параметры, включая SECRET_KEY
