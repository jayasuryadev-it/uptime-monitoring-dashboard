from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.monitors import router as monitors_router
from app.api.health_checks import router as health_checks_router
from app.api.dashboard import router as dashboard_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(monitors_router)
api_router.include_router(health_checks_router)
api_router.include_router(dashboard_router)
