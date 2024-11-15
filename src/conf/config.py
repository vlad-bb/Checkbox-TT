from typing import Any

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://DB_USERNAME:DB_PASSWORD@BD_HOST:5432/DB_NAME"
    SECRET_KEY_JWT: str = "1234567890"
    ALGORITHM: str = "HS256"
    HOST: str = 'localhost'
    PORT: int = 8000
    PROTOCOL: str = 'http'
    DOMAIN: str = f"{PROTOCOL}://{HOST}:{PORT}"

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()
