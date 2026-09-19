from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.monitor import Monitor


class MonitorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id_and_user(self, monitor_id: str, user_id: str) -> Optional[Monitor]:
        result = await self.db.execute(
            select(Monitor).where(Monitor.id == monitor_id, Monitor.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, monitor_id: str) -> Optional[Monitor]:
        result = await self.db.execute(select(Monitor).where(Monitor.id == monitor_id))
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: str) -> List[Monitor]:
        result = await self.db.execute(
            select(Monitor).where(Monitor.user_id == user_id).order_by(Monitor.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_all_active(self) -> List[Monitor]:
        result = await self.db.execute(select(Monitor).where(Monitor.is_active == True))
        return list(result.scalars().all())

    async def create(self, user_id: str, name: str, url: str, interval: int = 60, timeout: int = 10) -> Monitor:
        monitor = Monitor(
            user_id=user_id,
            name=name,
            url=url,
            interval=interval,
            timeout=timeout,
            is_active=True
        )
        self.db.add(monitor)
        await self.db.commit()
        await self.db.refresh(monitor)
        return monitor

    async def update(self, monitor: Monitor, **kwargs) -> Monitor:
        for key, value in kwargs.items():
            if value is not None and hasattr(monitor, key):
                setattr(monitor, key, value)
        await self.db.commit()
        await self.db.refresh(monitor)
        return monitor

    async def delete(self, monitor: Monitor) -> None:
        await self.db.delete(monitor)
        await self.db.commit()
