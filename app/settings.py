from typing import Optional

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Postgres
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    SQLALCHEMY_DATABASE_URI: str = ""

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, values: ValidationInfo) -> str:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            path=values.data.get("POSTGRES_DB"),
        ).unicode_string()

    # MinIO
    MINIO_ROOT_USER: Optional[str] = "admin"
    MINIO_ROOT_PASSWORD: Optional[str] = "Admin@123"
    MINIO_DEFAULT_BUCKET: Optional[str] = "football-data-platform"

    # AWS
    AWS_BUCKET_NAME: str = "football-data-platform"
    AWS_ACCESS_KEY_ID: str = "admin"
    AWS_SECRET_ACCESS_KEY: str = "Admin@123"
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: Optional[str] = "http://localhost:9000"


settings: Settings = Settings()
