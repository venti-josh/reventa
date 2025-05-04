from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate


class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> list[Link]:
        result = await db.execute(select(Link).where(Link.org_id == org_id))
        return result.scalars().all()

    async def get_by_survey_instance_id(
        self, db: AsyncSession, *, survey_instance_id: UUID
    ) -> list[Link]:
        result = await db.execute(
            select(Link).where(Link.survey_instance_id == survey_instance_id)
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, *, id: UUID) -> Link | None:
        """
        Get a link by its ID and validate it's not expired
        """
        from datetime import datetime

        now = datetime.now()
        result = await db.execute(
            select(Link)
            .where(Link.id == id)
            .where((Link.expires_at > now) | (Link.expires_at.is_(None)))
        )
        return result.scalar_one_or_none()

    async def get_active_links(self, db: AsyncSession, *, org_id: UUID) -> list[Link]:
        from datetime import datetime

        from sqlalchemy import or_

        now = datetime.now()
        result = await db.execute(
            select(Link)
            .where(Link.org_id == org_id)
            .where(or_(Link.expires_at > now, Link.expires_at.is_(None)))
        )
        return result.scalars().all()


link_crud = CRUDLink(Link)
