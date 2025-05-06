from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.org_allowed_domain import OrgAllowedDomain
from app.schemas.org_allowed_domain import (
    OrgAllowedDomainCreate,
    OrgAllowedDomainUpdate,
)


class CRUDOrgAllowedDomain(CRUDBase[OrgAllowedDomain, OrgAllowedDomainCreate, OrgAllowedDomainUpdate]):
    async def get_by_domain(self, db: AsyncSession, *, domain: str) -> OrgAllowedDomain | None:
        result = await db.execute(select(OrgAllowedDomain).where(OrgAllowedDomain.domain == domain))
        return result.scalar_one_or_none()

    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> Sequence[OrgAllowedDomain]:
        result = await db.execute(select(OrgAllowedDomain).where(OrgAllowedDomain.org_id == org_id))
        return result.scalars().all()


org_allowed_domain_crud = CRUDOrgAllowedDomain(OrgAllowedDomain)
