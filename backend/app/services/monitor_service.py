from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.monitor_repo import MonitorRepository
from app.repositories.health_check_repo import HealthCheckRepository
from app.repositories.incident_repo import IncidentRepository
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate, MonitorUpdate, MonitorResponse
from app.schemas.dashboard import DashboardSummary, MonitorDetailResponse
from app.schemas.health_check import HealthCheckResponse
from app.schemas.incident import IncidentResponse


class MonitorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.monitor_repo = MonitorRepository(db)
        self.health_check_repo = HealthCheckRepository(db)
        self.incident_repo = IncidentRepository(db)

    async def create_monitor(self, user_id: str, data: MonitorCreate) -> MonitorResponse:
        monitor = await self.monitor_repo.create(
            user_id=user_id,
            name=data.name,
            url=data.url,
            interval=data.interval,
            timeout=data.timeout
        )
        return await self._to_monitor_response(monitor)

    async def list_user_monitors(self, user_id: str) -> List[MonitorResponse]:
        monitors = await self.monitor_repo.list_by_user(user_id)
        responses = []
        for m in monitors:
            responses.append(await self._to_monitor_response(m))
        return responses

    async def get_user_monitor(self, monitor_id: str, user_id: str) -> Monitor:
        monitor = await self.monitor_repo.get_by_id_and_user(monitor_id, user_id)
        if not monitor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Monitor not found or unauthorized access"
            )
        return monitor

    async def get_monitor_detail(self, monitor_id: str, user_id: str) -> MonitorDetailResponse:
        monitor = await self.get_user_monitor(monitor_id, user_id)
        monitor_resp = await self._to_monitor_response(monitor)

        recent_checks = await self.health_check_repo.list_by_monitor(monitor_id, limit=50)
        incidents = await self.incident_repo.list_by_monitor(monitor_id, limit=50)

        # Compute uptime percentage for this monitor
        total_checks = len(recent_checks)
        if total_checks > 0:
            up_count = sum(1 for c in recent_checks if c.status == "UP")
            uptime_pct = round((up_count / total_checks) * 100.0, 2)
        else:
            uptime_pct = 100.0

        return MonitorDetailResponse(
            monitor=monitor_resp,
            uptime_percentage=uptime_pct,
            recent_checks=[HealthCheckResponse.model_validate(c) for c in recent_checks],
            incidents=[IncidentResponse.model_validate(inc) for inc in incidents]
        )

    async def update_monitor(self, monitor_id: str, user_id: str, data: MonitorUpdate) -> MonitorResponse:
        monitor = await self.get_user_monitor(monitor_id, user_id)
        updated = await self.monitor_repo.update(
            monitor,
            name=data.name,
            url=data.url,
            interval=data.interval,
            timeout=data.timeout,
            is_active=data.is_active
        )
        return await self._to_monitor_response(updated)

    async def delete_monitor(self, monitor_id: str, user_id: str) -> None:
        monitor = await self.get_user_monitor(monitor_id, user_id)
        await self.monitor_repo.delete(monitor)

    async def get_dashboard_summary(self, user_id: str) -> DashboardSummary:
        monitors = await self.monitor_repo.list_by_user(user_id)
        monitor_responses = []

        total = len(monitors)
        up_count = 0
        down_count = 0
        paused_count = 0
        all_checks_up = 0
        total_checks_count = 0

        for m in monitors:
            m_resp = await self._to_monitor_response(m)
            monitor_responses.append(m_resp)

            if not m.is_active:
                paused_count += 1
            elif m_resp.last_status == "UP":
                up_count += 1
            elif m_resp.last_status == "DOWN":
                down_count += 1

            checks = await self.health_check_repo.list_by_monitor(m.id, limit=50)
            if checks:
                all_checks_up += sum(1 for c in checks if c.status == "UP")
                total_checks_count += len(checks)

        overall_uptime = (
            round((all_checks_up / total_checks_count) * 100.0, 2)
            if total_checks_count > 0
            else 100.0
        )

        return DashboardSummary(
            total_monitors=total,
            up_monitors=up_count,
            down_monitors=down_count,
            paused_monitors=paused_count,
            overall_uptime_percentage=overall_uptime,
            monitors=monitor_responses
        )

    async def _to_monitor_response(self, monitor: Monitor) -> MonitorResponse:
        latest_check = await self.health_check_repo.get_latest_by_monitor(monitor.id)
        last_status = latest_check.status if latest_check else "UNKNOWN"
        last_response_time = latest_check.response_time if latest_check else None
        last_checked_at = latest_check.checked_at if latest_check else None

        resp = MonitorResponse.model_validate(monitor)
        resp.last_status = last_status
        resp.last_response_time = last_response_time
        resp.last_checked_at = last_checked_at
        return resp
