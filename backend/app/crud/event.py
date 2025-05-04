from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> list[Event]:
        result = await db.execute(select(Event).where(Event.org_id == org_id))
        return result.scalars().all()

    async def get_by_name(
        self, db: AsyncSession, *, name: str, org_id: UUID
    ) -> Event | None:
        result = await db.execute(
            select(Event).where(Event.name == name).where(Event.org_id == org_id)
        )
        return result.scalar_one_or_none()

    async def get_active_events(self, db: AsyncSession, *, org_id: UUID) -> list[Event]:
        from datetime import datetime

        now = datetime.now()
        result = await db.execute(
            select(Event)
            .where(Event.org_id == org_id)
            .where(Event.start_dt <= now)
            .where(Event.end_dt >= now)
        )
        return result.scalars().all()

    async def get_by_status(
        self, db: AsyncSession, *, status: str, org_id: UUID
    ) -> list[Event]:
        result = await db.execute(
            select(Event).where(Event.status == status).where(Event.org_id == org_id)
        )
        return result.scalars().all()


event_crud = CRUDEvent(Event)
