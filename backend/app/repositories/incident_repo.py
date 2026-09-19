from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.incident import Incident


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_by_monitor(self, monitor_id: str) -> Optional[Incident]:
        result = await self.db.execute(
            select(Incident).where(
                Incident.monitor_id == monitor_id,
                Incident.resolved_at.is_(None)
            ).order_by(Incident.started_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def create(self, monitor_id: str, reason: str) -> Incident:
        incident = Incident(
            monitor_id=monitor_id,
            reason=reason,
            started_at=utc_now()
        )
        self.db.add(incident)
        await self.db.commit()
        await self.db.refresh(incident)
        return incident

    async def resolve(self, incident: Incident) -> Incident:
        incident.resolved_at = utc_now()
        await self.db.commit()
        await self.db.refresh(incident)
        return incident

    async def list_by_monitor(self, monitor_id: str, limit: int = 50) -> List[Incident]:
        result = await self.db.execute(
            select(Incident)
            .where(Incident.monitor_id == monitor_id)
            .order_by(Incident.started_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
