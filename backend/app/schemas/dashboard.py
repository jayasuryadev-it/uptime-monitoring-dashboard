from typing import List, Optional
from pydantic import BaseModel
from app.schemas.monitor import MonitorResponse
from app.schemas.health_check import HealthCheckResponse
from app.schemas.incident import IncidentResponse


class DashboardSummary(BaseModel):
    total_monitors: int
    up_monitors: int
    down_monitors: int
    paused_monitors: int
    overall_uptime_percentage: float
    monitors: List[MonitorResponse]


class MonitorDetailResponse(BaseModel):
    monitor: MonitorResponse
    uptime_percentage: float
    recent_checks: List[HealthCheckResponse]
    incidents: List[IncidentResponse]
