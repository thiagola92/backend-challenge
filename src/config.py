import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Better throw error now than later.
    postgres_dsn: PostgresDsn = os.environ["POSTGRES_DSN"]
    api_username: str = os.environ["API_USERNAME"]
    api_password: str = os.environ["API_PASSWORD"]

    # Security.
    secret_key: str = os.environ["SECRET_KEY"]
    algorithm_to_sign_jwt: str = "HS256"
    access_token_duration_minutes: int = 30


settings = Settings()
