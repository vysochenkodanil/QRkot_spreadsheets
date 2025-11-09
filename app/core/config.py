from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Cat Charity Fund"
    database_url: str = "sqlite+aiosqlite:///./charity.db"
    secret: str = "SECRET"
    password_len: int = 3
    minute: int = 3600
    # Google API Settings
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    token_uri: str = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: str = (
        "https://www.googleapis.com/oauth2/v1/certs"
    )
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
