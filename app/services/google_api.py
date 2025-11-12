from typing import List
from aiogoogle import Aiogoogle

from app.core.config import settings, google_constants
from app.models.charity_project import CharityProject


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать новую Google таблицу."""
    service = await wrapper_services.discover("sheets", "v4")

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=google_constants.SPREADSHEET_BODY)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
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
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    """Обновить данные в таблице."""
    service = await wrapper_services.discover("sheets", "v4")

    table_values = google_constants.TABLE_HEADERS.copy()

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

    update_body = {**google_constants.UPDATE_BODY_BASE, "values": table_values}

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=google_constants.RANGE,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
