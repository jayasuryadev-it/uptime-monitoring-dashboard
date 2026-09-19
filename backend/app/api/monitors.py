from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.schemas.monitor import MonitorCreate, MonitorUpdate, MonitorResponse
from app.schemas.dashboard import MonitorDetailResponse
from app.schemas.health_check import HealthCheckResponse
from app.services.monitor_service import MonitorService
from app.services.checker_service import CheckerService

router = APIRouter(prefix="/monitors", tags=["Monitors"])


@router.get("", response_model=List[MonitorResponse])
async def list_monitors(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    return await service.list_user_monitors(current_user.id)


@router.post("", response_model=MonitorResponse, status_code=status.HTTP_201_CREATED)
async def create_monitor(
    data: MonitorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    return await service.create_monitor(current_user.id, data)


@router.get("/{monitor_id}", response_model=MonitorDetailResponse)
async def get_monitor_detail(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    return await service.get_monitor_detail(monitor_id, current_user.id)


@router.put("/{monitor_id}", response_model=MonitorResponse)
async def update_monitor(
    monitor_id: str,
    data: MonitorUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    return await service.update_monitor(monitor_id, current_user.id, data)


@router.delete("/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monitor(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    await service.delete_monitor(monitor_id, current_user.id)


@router.post("/{monitor_id}/check", response_model=HealthCheckResponse)
async def trigger_health_check(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    monitor = await service.get_user_monitor(monitor_id, current_user.id)
    checker = CheckerService(db)
    check = await checker.perform_check(monitor)
    return HealthCheckResponse.model_validate(check)


@router.patch("/{monitor_id}/toggle", response_model=MonitorResponse)
async def toggle_monitor_status(
    monitor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MonitorService(db)
    monitor = await service.get_user_monitor(monitor_id, current_user.id)
    new_status = not monitor.is_active
    update_data = MonitorUpdate(is_active=new_status)
    return await service.update_monitor(monitor_id, current_user.id, update_data)
