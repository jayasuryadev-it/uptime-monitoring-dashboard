from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class HealthCheckResponse(BaseModel):
    id: str
    monitor_id: str
    status: str
    status_code: Optional[int] = None
    response_time: float
    error_message: Optional[str] = None
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)
