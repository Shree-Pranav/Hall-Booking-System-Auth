from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    DATABASE_URL: str | None = None

    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    s = Settings()

    # If a full DATABASE_URL isn't provided, or it points at localhost from
    # the developer .env while the container provides a real DB host (eg `db`),
    # prefer building the URL from the DB_* values so the service can connect.
    rebuild = False
    if not s.DATABASE_URL:
        rebuild = True
    else:
        # If DATABASE_URL contains localhost but DB_HOST is set to a different
        # host (for example the docker-compose service name `db`), rebuild it.
        lower_db_url = s.DATABASE_URL.lower()
        if ("localhost" in lower_db_url or "127.0.0.1" in lower_db_url) and s.DB_HOST and s.DB_HOST not in (
            "localhost",
            "127.0.0.1",
        ):
            rebuild = True

    if rebuild:
        s.DATABASE_URL = (
            f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"
        )

    return s


settings = get_settings()