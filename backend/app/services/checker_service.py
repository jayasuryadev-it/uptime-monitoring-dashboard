import time
import httpx
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.monitor import Monitor
from app.models.health_check import HealthCheck
from app.repositories.health_check_repo import HealthCheckRepository
from app.repositories.incident_repo import IncidentRepository


class CheckerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.health_check_repo = HealthCheckRepository(db)
        self.incident_repo = IncidentRepository(db)

    async def perform_check(self, monitor: Monitor) -> HealthCheck:
        start_time = time.perf_counter()
        status = "DOWN"
        status_code: Optional[int] = None
        error_message: Optional[str] = None

        timeout_sec = float(monitor.timeout)

        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_sec) as client:
                response = await client.get(
                    monitor.url,
                    headers={"User-Agent": "UptimeMonitorBot/1.0"}
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                status_code = response.status_code

                if 200 <= status_code < 400:
                    status = "UP"
                else:
                    status = "DOWN"
                    error_message = f"HTTP status code {status_code}"

        except httpx.TimeoutException:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            status = "DOWN"
            error_message = f"Request timed out after {monitor.timeout}s"
        except httpx.RequestError as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            status = "DOWN"
            error_message = f"Network connection error: {str(exc)}"
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            status = "DOWN"
            error_message = f"Unexpected error: {str(exc)}"

        # Save health check record
        health_check = await self.health_check_repo.create(
            monitor_id=monitor.id,
            status=status,
            status_code=status_code,
            response_time=round(elapsed_ms, 2),
            error_message=error_message
        )

        # Handle Incident lifecycle: UP -> DOWN creates incident, DOWN -> UP resolves active incident
        await self._manage_incidents(monitor, status, error_message or "Monitor reported DOWN status")

        return health_check

    async def _manage_incidents(self, monitor: Monitor, current_status: str, reason: str):
        active_incident = await self.incident_repo.get_active_by_monitor(monitor.id)

        if current_status == "DOWN":
            if not active_incident:
                # Transition UP -> DOWN: Create new incident
                await self.incident_repo.create(monitor_id=monitor.id, reason=reason)
        elif current_status == "UP":
            if active_incident:
                # Transition DOWN -> UP: Resolve active incident
                await self.incident_repo.resolve(active_incident)
