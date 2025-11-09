from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models.charity_project import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать новую Google таблицу."""
    service = await wrapper_services.discover("sheets", "v4")

    spreadsheet_body = {
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

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    """Выдать права на доступ к таблице."""
    service = await wrapper_services.discover("drive", "v3")

    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: List[CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    """Обновить данные в таблице."""
    service = await wrapper_services.discover("sheets", "v4")

    table_values = [
        ["Отчет по закрытым проектам"],
        ["Топ проектов по скорости сборов"],
        [
            "Название проекта",
            "Время сбора (дней)",
            "Описание",
            "Собрано средств",
        ],
    ]

    for project in projects:
        collection_time = (project.close_date - project.create_date).days
        table_values.append(
            [
                project.name,
                str(collection_time),
                project.description,
                str(project.full_amount),
            ]
        )

    update_body = {"majorDimension": "ROWS", "values": table_values}

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:D30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
