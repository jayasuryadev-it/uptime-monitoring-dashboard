from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.schemas.health_check import HealthCheckResponse
from app.services.monitor_service import MonitorService
from app.repositories.health_check_repo import HealthCheckRepository

router = APIRouter(prefix="/health-checks", tags=["Health Checks"])


@router.get("/monitors/{monitor_id}", response_model=List[HealthCheckResponse])
async def list_health_checks(
    monitor_id: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    monitor_service = MonitorService(db)
    # Enforce user authorization check on monitor
    await monitor_service.get_user_monitor(monitor_id, current_user.id)

    hc_repo = HealthCheckRepository(db)
    checks = await hc_repo.list_by_monitor(monitor_id, limit=limit)
    return [HealthCheckResponse.model_validate(c) for c in checks]
