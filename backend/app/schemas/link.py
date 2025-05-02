from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LinkBase(BaseModel):
    org_id: UUID
    survey_instance_id: UUID
    expires_at: datetime | None = None


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    org_id: UUID | None = None
    survey_instance_id: UUID | None = None
    expires_at: datetime | None = None


class LinkRead(LinkBase):
    id: UUID

    model_config = {"from_attributes": True}
