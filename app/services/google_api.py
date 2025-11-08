import json
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings
from app.models import CharityProject

# Константы
FORMAT = "%Y/%m/%d %H:%M:%S"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Учетные данные из настроек
INFO = {
    "type": settings.type,
    "project_id": settings.project_id,
    "private_key_id": settings.private_key_id,
    "private_key": settings.private_key.replace('\\n', '\n') if settings.private_key else None,
    "client_email": settings.client_email,
    "client_id": settings.client_id,
    "auth_uri": settings.auth_uri,
    "token_uri": settings.token_uri,
    "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url,
    "client_x509_cert_url": settings.client_x509_cert_url,
}

async def get_service():
    """Получить сервис для работы с Google API."""
    creds = ServiceAccountCreds(scopes=SCOPES, **INFO)
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        yield aiogoogle

async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать новую Google таблицу."""
    service = await wrapper_services.discover('sheets', 'v4')
    
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет по закрытым проектам',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Закрытые проекты',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 4
                }
            }
        }]
    }
    
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid

async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    """Выдать права на доступ к таблице."""
    service = await wrapper_services.discover('drive', 'v3')
    
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )

async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: List[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    """Обновить данные в таблице."""
    service = await wrapper_services.discover('sheets', 'v4')
    
    # Заголовки таблицы
    table_values = [
        ['Отчет по закрытым проектам'],
        ['Топ проектов по скорости сборов'],
        ['Название проекта', 'Время сбора (дней)', 'Описание', 'Собрано средств']
    ]
    
    # Данные проектов
    for project in projects:
        # Вычисляем время сбора в днях
        collection_time = (project.close_date - project.create_date).days
        table_values.append([
            project.name,
            str(collection_time),
            project.description,
            str(project.full_amount)
        ])
    
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:D30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )