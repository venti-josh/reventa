import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.event import event_crud
from app.crud.survey import survey_crud
from app.crud.survey_instance import survey_instance_crud
from app.db.session import get_async_session
from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.schemas.survey_instance import SurveyInstanceCreate, SurveyInstanceRead

router = APIRouter()


@router.post("/", response_model=EventRead)
async def create_event(
    *,
    event_in: EventCreate,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Create a new event."""
    event = await event_crud.create(db, obj_in=event_in)
    return event


@router.get("/", response_model=list[EventRead])
async def get_events(
    db: AsyncSession = Depends(get_async_session),
    org_id: int | None = None,
) -> list[EventRead]:
    """List events filtered by organization if org_id is provided."""
    if org_id:
        # Convert integer org_id to UUID
        org_uuid = uuid.UUID(int=org_id) if isinstance(org_id, int) else uuid.UUID(org_id)
        events = await event_crud.get_by_org_id(db, org_id=org_uuid)
    else:
        events = await event_crud.get_multi(db)
    return events


@router.get("/{id}", response_model=EventRead)
async def get_event(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Get event details by ID."""
    # Convert integer id to UUID
    event_uuid = uuid.UUID(int=id) if isinstance(id, int) else uuid.UUID(id)
    event = await event_crud.get(db, id=event_uuid)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )
    return event


@router.patch("/{id}", response_model=EventRead)
async def update_event(
    *,
    id: int,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Update an event."""
    # Convert integer id to UUID
    event_uuid = uuid.UUID(int=id) if isinstance(id, int) else uuid.UUID(id)
    event = await event_crud.get(db, id=event_uuid)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )
    event = await event_crud.update(db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/{id}", response_model=EventRead)
async def delete_event(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Delete an event."""
    # Convert integer id to UUID
    event_uuid = uuid.UUID(int=id) if isinstance(id, int) else uuid.UUID(id)
    event = await event_crud.get(db, id=event_uuid)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )
    event = await event_crud.remove(db, id=event_uuid)
    return event


@router.post("/{id}/surveys/{survey_id}/launch", response_model=SurveyInstanceRead)
async def launch_survey(
    *,
    id: int,
    survey_id: int,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyInstanceRead:
    """Launch a survey for an event by creating a survey instance."""
    # Convert integer ids to UUIDs
    event_uuid = uuid.UUID(int=id) if isinstance(id, int) else uuid.UUID(id)
    survey_uuid = uuid.UUID(int=survey_id) if isinstance(survey_id, int) else uuid.UUID(survey_id)

    # Verify event exists
    event = await event_crud.get(db, id=event_uuid)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    # Verify survey exists
    survey = await survey_crud.get(db, id=survey_uuid)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )

    # Create survey instance
    survey_instance_in = SurveyInstanceCreate(
        event_id=event_uuid,
        survey_id=survey_uuid,
        is_active=True,
    )
    survey_instance = await survey_instance_crud.create(db, obj_in=survey_instance_in)
    return survey_instance
