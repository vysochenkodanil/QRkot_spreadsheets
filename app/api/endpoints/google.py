from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import get_projects_by_completion_rate
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
    summary="Создать отчет в Google Таблицах",
    description="Создает отчет с закрытыми проектами"
                "отсортированными по скорости сбора средств",
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Создать отчет в Google Таблицах."""
    projects = await get_projects_by_completion_rate(session)
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services)

    return {
        "msg": "Отчет успешно сформирован",
        "spreadsheet_url":
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
        "projects_count": len(projects),
    }
