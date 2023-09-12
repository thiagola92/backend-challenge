from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Alert(BaseModel):
    id: str = Field(examples=[uuid4()])
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    camera_id: str = Field(examples=[uuid4()])

    model_config = ConfigDict(from_attributes=True)

    @field_validator("occurred_at", mode="after")
    @classmethod
    def date_without_timezone(cls, dt: datetime) -> datetime:
        return datetime.combine(dt.date(), dt.time())
