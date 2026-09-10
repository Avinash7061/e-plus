from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Loads config from environment variables / a .env file.

    supabase_db_url should be the direct Postgres connection string from
    Supabase (Project Settings -> Database -> Connection string -> URI),
    rewritten to use the asyncpg driver, e.g.:

        postgresql+asyncpg://postgres:<password>@<host>:5432/postgres

    Don't commit the real .env -- only .env.example should be tracked.
    """

    supabase_db_url: str
    supabase_url: str | None = None        # REST endpoint, only needed if you also use supabase-py
    supabase_service_key: str | None = None

    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    fcm_server_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
