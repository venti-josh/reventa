from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_email
from app.crud.link import link_crud
from app.crud.survey_response import survey_response_crud
from app.db.session import get_async_session
from app.schemas.survey_response import SurveyResponseCreate, SurveyResponseRead

router = APIRouter()


@router.get("/{uuid}")
async def get_public_form(
    *,
    uuid: str,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Fetch form schema and metadata for a public survey link."""
    # Look up the link by UUID
    try:
        uuid_obj = UUID(uuid)
        link = await link_crud.get_by_id(db, id=uuid_obj)
    except ValueError as err:
        raise HTTPException(
            status_code=404,
            detail="Invalid UUID format",
        ) from err

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Survey link not found",
        )

    # Get the survey instance
    survey_instance = link.survey_instance
    if not survey_instance:
        raise HTTPException(
            status_code=404,
            detail="Survey is not available",
        )

    # Get the survey schema
    survey = survey_instance.survey

    # Return the survey schema and metadata
    return {
        "title": survey.title,
        "schema": survey.schema,
        "event": {
            "name": survey_instance.event.name,
            "start_dt": survey_instance.event.start_dt,
            "end_dt": survey_instance.event.end_dt,
        },
    }


@router.post("/{uuid}/submit", response_model=SurveyResponseRead)
async def submit_survey_response(
    *,
    uuid: str,
    response_data: dict[str, Any],
    db: AsyncSession = Depends(get_async_session),
) -> SurveyResponseRead:
    """Submit answers for a survey."""
    # Look up the link by UUID
    try:
        uuid_obj = UUID(uuid)
        link = await link_crud.get_by_id(db, id=uuid_obj)
    except ValueError as err:
        raise HTTPException(
            status_code=404,
            detail="Invalid UUID format",
        ) from err

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Survey link not found",
        )

    # Get the survey instance
    survey_instance = link.survey_instance
    if not survey_instance:
        raise HTTPException(
            status_code=404,
            detail="Survey is not available",
        )

    # Extract data from request
    answers = response_data.get("answers", {})
    email = response_data.get("email")
    if email:
        email_hash = hash_email(email)
    else:
        email_hash = None

    # Create survey response
    response_in = SurveyResponseCreate(
        survey_instance_id=survey_instance.id,
        answers=answers,
        email_hash=email_hash,
        org_id=survey_instance.org_id,
    )

    response = await survey_response_crud.create(db, obj_in=response_in)
    return response
