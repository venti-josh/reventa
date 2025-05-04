from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.event import EventStatus


class EventBase(BaseModel):
    name: str
    description: str | None = None
    start_dt: datetime
    end_dt: datetime
    status: EventStatus
    org_id: UUID


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_dt: datetime | None = None
    end_dt: datetime | None = None
    status: EventStatus | None = None
    org_id: UUID | None = None


class EventRead(EventBase):
    id: UUID

    model_config = {"from_attributes": True}
