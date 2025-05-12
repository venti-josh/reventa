import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.event import event_crud
from app.crud.survey import survey_crud
from app.db.session import get_async_session
from app.models.survey_instance import EmailRequirement
from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.schemas.survey_instance import SurveyInstanceRead

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
    id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Get event details by ID."""
    event = await event_crud.get(db, id=id)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )
    return event


@router.patch("/{id}", response_model=EventRead)
async def update_event(
    *,
    id: uuid.UUID,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Update an event."""
    event = await event_crud.get(db, id=id)
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
    id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
) -> EventRead:
    """Delete an event."""
    event = await event_crud.get(db, id=id)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )
    event = await event_crud.remove(db, id=id)
    return event


@router.post("/{id}/surveys/{survey_id}/launch", response_model=SurveyInstanceRead)
async def launch_survey(
    *,
    id: uuid.UUID,
    survey_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyInstanceRead:
    """Launch a survey for an event by creating a survey instance."""
    # Verify event exists
    event = await event_crud.get(db, id=id)
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    # Verify survey exists
    survey = await survey_crud.get(db, id=survey_id)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )

    # Create a new instance of the SurveyInstance model directly to ensure enum is handled correctly
    from app.models.survey_instance import SurveyInstance

    # Create the object directly with SQLAlchemy models
    db_obj = SurveyInstance(
        event_id=id,
        survey_id=survey_id,
        org_id=survey.org_id,
        email_requirement=EmailRequirement.NONE,  # Use the enum directly
    )

    # Add to session and commit
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    # Convert to read schema and return
    return SurveyInstanceRead.model_validate(db_obj)
