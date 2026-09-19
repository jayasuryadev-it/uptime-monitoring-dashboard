from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, field_validator, ConfigDict
from app.schemas.health_check import HealthCheckResponse


class MonitorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=2048)
    interval: int = Field(default=60, ge=10, le=86400)
    timeout: int = Field(default=10, ge=1, le=120)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v_str = str(v).strip()
        if not (v_str.startswith("http://") or v_str.startswith("https://")):
            v_str = "https://" + v_str
        return v_str


class MonitorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = Field(None, min_length=1, max_length=2048)
    interval: Optional[int] = Field(None, ge=10, le=86400)
    timeout: Optional[int] = Field(None, ge=1, le=120)
    is_active: Optional[bool] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v_str = str(v).strip()
        if not (v_str.startswith("http://") or v_str.startswith("https://")):
            v_str = "https://" + v_str
        return v_str


class MonitorResponse(BaseModel):
    id: str
    user_id: str
    name: str
    url: str
    interval: int
    timeout: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_status: Optional[str] = "UNKNOWN"
    last_response_time: Optional[float] = None
    last_checked_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
