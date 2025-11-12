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


class GoogleConstants:
    """Константы для работы с Google API."""

    DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

    RANGE = "A1:D30"

    SPREADSHEET_BODY = {
        "properties": {
            "title": "Отчет по закрытым проектам",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Закрытые проекты",
                    "gridProperties": {"rowCount": 100, "columnCount": 4},
                }
            }
        ],
    }

    UPDATE_BODY_BASE = {"majorDimension": "ROWS"}

    TABLE_HEADERS = [
        ["Отчет по закрытым проектам"],
        ["Топ проектов по скорости сборов"],
        [
            "Название проекта",
            "Время сбора (дней)",
            "Описание",
            "Собрано средств",
        ],
    ]


settings = Settings()
google_constants = GoogleConstants()
