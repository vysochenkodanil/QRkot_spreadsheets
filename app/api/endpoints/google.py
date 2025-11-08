from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import get_projects_by_completion_rate
from app.services.google_api import (
    get_service,
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value
)
from aiogoogle import Aiogoogle

router = APIRouter(prefix='/google', tags=['Google'])

@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    summary='Создать отчет в Google Таблицах',
    description='Создает отчет с закрытыми проектами, отсортированными по скорости сбора средств'
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Создать отчет в Google Таблицах."""
    # Получаем отсортированные проекты
    projects = await get_projects_by_completion_rate(session)
    
    # Создаем таблицу
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    
    # Выдаем права доступа
    await set_user_permissions(spreadsheet_id, wrapper_services)

    # Заполняем таблицу данными
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services)
    
    return {
        "msg": "Отчет успешно сформирован",
        "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
        "projects_count": len(projects)
    }
