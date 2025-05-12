from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.event import Event, EventStatus
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: EventCreate) -> Event:
        # Convert datetime strings to datetime objects if needed
        obj_in_data = obj_in.model_dump()
        if isinstance(obj_in_data["start_dt"], str):
            obj_in_data["start_dt"] = datetime.fromisoformat(obj_in_data["start_dt"].replace("Z", "+00:00"))
        if isinstance(obj_in_data["end_dt"], str):
            obj_in_data["end_dt"] = datetime.fromisoformat(obj_in_data["end_dt"].replace("Z", "+00:00"))

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_org_id(self, db: AsyncSession, *, org_id: UUID) -> Sequence[Event]:
        result = await db.execute(select(Event).where(Event.org_id == org_id))
        return result.scalars().all()

    async def get_by_name(self, db: AsyncSession, *, name: str, org_id: UUID) -> Event | None:
        result = await db.execute(select(Event).where(Event.name == name).where(Event.org_id == org_id))
        return result.scalar_one_or_none()

    async def get_active_events(self, db: AsyncSession, *, org_id: UUID) -> Sequence[Event]:
        now = datetime.now()
        result = await db.execute(
            select(Event).where(Event.org_id == org_id).where(Event.start_dt <= now).where(Event.end_dt >= now)
        )
        return result.scalars().all()

    async def get_by_status(self, db: AsyncSession, *, status: EventStatus, org_id: UUID) -> Sequence[Event]:
        result = await db.execute(select(Event).where(Event.status == status).where(Event.org_id == org_id))
        return result.scalars().all()


event_crud = CRUDEvent(Event)
