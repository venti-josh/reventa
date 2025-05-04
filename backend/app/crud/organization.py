from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Organization | None:
        result = await db.execute(select(Organization).where(Organization.name == name))
        return result.scalar_one_or_none()


organization_crud = CRUDOrganization(Organization)
