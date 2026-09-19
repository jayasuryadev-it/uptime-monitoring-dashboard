from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.monitor_service import MonitorService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    return await service.get_dashboard_summary(current_user.id)
