from fastapi import APIRouter

from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.google import router as google_router

api_router = APIRouter()

api_router.include_router(
    charity_project_router,
    prefix="/charity_project",
    tags=["Charity Projects"],
)

api_router.include_router(
    donation_router,
    prefix="/donation",
    tags=["Donations"],
)

api_router.include_router(google_router, prefix="/google", tags=["Google"])

__all__ = ["api_router"]
