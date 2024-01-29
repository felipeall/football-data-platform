from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    AWS_BUCKET_NAME: str = "football-data-platform"
    AWS_ACCESS_KEY_ID: str = "admin"
    AWS_SECRET_ACCESS_KEY: str = "Admin@123"
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: Optional[str] = "http://localhost:9000"


settings: Settings = Settings()
