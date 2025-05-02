from uuid import UUID

from pydantic import BaseModel


class OrgAllowedDomainBase(BaseModel):
    domain: str
    org_id: UUID


class OrgAllowedDomainCreate(OrgAllowedDomainBase):
    pass


class OrgAllowedDomainUpdate(BaseModel):
    domain: str | None = None
    org_id: UUID | None = None


class OrgAllowedDomainRead(OrgAllowedDomainBase):
    id: UUID

    model_config = {"from_attributes": True}
