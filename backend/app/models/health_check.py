import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class HealthCheck(Base):
    __tablename__ = "health_checks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    monitor_id: Mapped[str] = mapped_column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)  # "UP" or "DOWN"
    status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # ms
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)

    monitor: Mapped["Monitor"] = relationship("Monitor", back_populates="health_checks")
