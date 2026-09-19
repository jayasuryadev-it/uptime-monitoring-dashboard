from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class IncidentResponse(BaseModel):
    id: str
    monitor_id: str
    started_at: datetime
    resolved_at: Optional[datetime] = None
    reason: str

    model_config = ConfigDict(from_attributes=True)
