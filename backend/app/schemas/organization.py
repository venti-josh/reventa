from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
