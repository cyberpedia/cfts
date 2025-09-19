import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Core application settings
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Email settings
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME", "username")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD", "password")
    MAIL_FROM: str = os.environ.get("MAIL_FROM", "noreply@example.com")
    MAIL_PORT: int = int(os.environ.get("MAIL_PORT", 587))
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER", "smtp.example.com")
    MAIL_STARTTLS: bool = os.environ.get("MAIL_STARTTLS", "True").lower() in ("true", "1", "t")
    MAIL_SSL_TLS: bool = os.environ.get("MAIL_SSL_TLS", "False").lower() in ("true", "1", "t")

    # OAuth settings for Google
    GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.environ.get("GOOGLE_CLIENT_SECRET", "")

    class Config:
        env_file = ".env"

settings = Settings()
