import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.survey import survey_crud
from app.db.session import get_async_session
from app.schemas.survey import SurveyCreate, SurveyRead, SurveyUpdate

router = APIRouter()


@router.post("/", response_model=SurveyRead)
async def create_survey(
    *,
    survey_in: SurveyCreate,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyRead:
    """Create a new survey with JSON schema."""
    survey = await survey_crud.create(db, obj_in=survey_in)
    return survey


@router.get("/", response_model=list[SurveyRead])
async def get_surveys(
    db: AsyncSession = Depends(get_async_session),
) -> list[SurveyRead]:
    """List all surveys."""
    surveys = await survey_crud.get_multi(db)
    return surveys


@router.get("/{id}", response_model=SurveyRead)
async def get_survey(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyRead:
    """Get survey details by ID."""
    # Convert integer id to UUID by first converting to string
    try:
        survey_uuid = uuid.UUID(str(id))
        survey = await survey_crud.get(db, id=survey_uuid)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format",
        ) from err

    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )
    return survey


@router.patch("/{id}", response_model=SurveyRead)
async def update_survey(
    *,
    id: int,
    survey_in: SurveyUpdate,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyRead:
    """Update a survey if it's not published."""
    # Convert integer id to UUID by first converting to string
    try:
        survey_uuid = uuid.UUID(str(id))
        survey = await survey_crud.get(db, id=survey_uuid)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format",
        ) from err

    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )

    if survey.is_published:
        raise HTTPException(
            status_code=400,
            detail="Cannot update a published survey",
        )

    survey = await survey_crud.update(db, db_obj=survey, obj_in=survey_in)
    return survey


@router.post("/{id}/publish", response_model=SurveyRead)
async def publish_survey(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> SurveyRead:
    """Publish a survey, marking it as unchangeable."""
    # Convert integer id to UUID by first converting to string
    try:
        survey_uuid = uuid.UUID(str(id))
        survey = await survey_crud.get(db, id=survey_uuid)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format",
        ) from err

    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found",
        )

    if survey.is_published:
        raise HTTPException(
            status_code=400,
            detail="Survey is already published",
        )

    # Update the is_published field
    survey_update = SurveyUpdate(is_published=True)
    survey = await survey_crud.update(db, db_obj=survey, obj_in=survey_update)
    return survey
