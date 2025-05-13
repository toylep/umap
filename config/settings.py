from pydantic_settings import BaseSettings
from pydantic import Field
from typing import ClassVar


class DBSettings(BaseSettings):
    postgres_db: str = Field(..., env="POSTGRES_DB")
    db_host: str = Field(..., env="DB_HOST")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_user: str = Field(..., env="POSTGRES_USER")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


class Settings(BaseSettings):
    db: ClassVar = DBSettings()
