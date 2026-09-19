from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.health_check import HealthCheck


class HealthCheckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        monitor_id: str,
        status: str,
        response_time: float,
        status_code: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> HealthCheck:
        check = HealthCheck(
            monitor_id=monitor_id,
            status=status,
            status_code=status_code,
            response_time=response_time,
            error_message=error_message
        )
        self.db.add(check)
        await self.db.commit()
        await self.db.refresh(check)
        return check

    async def get_latest_by_monitor(self, monitor_id: str) -> Optional[HealthCheck]:
        result = await self.db.execute(
            select(HealthCheck)
            .where(HealthCheck.monitor_id == monitor_id)
            .order_by(HealthCheck.checked_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_by_monitor(self, monitor_id: str, limit: int = 50) -> List[HealthCheck]:
        result = await self.db.execute(
            select(HealthCheck)
            .where(HealthCheck.monitor_id == monitor_id)
            .order_by(HealthCheck.checked_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
