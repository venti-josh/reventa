from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventBase(BaseModel):
    name: str
    description: str | None = None
    start_dt: datetime
    end_dt: datetime
    status: str
    org_id: UUID


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_dt: datetime | None = None
    end_dt: datetime | None = None
    status: str | None = None
    org_id: UUID | None = None


class EventRead(EventBase):
    id: UUID

    model_config = {"from_attributes": True}
