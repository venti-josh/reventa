import io
import uuid

import qrcode
import qrcode.image.svg
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.link import link_crud
from app.crud.survey_instance import survey_instance_crud
from app.crud.survey_response import survey_response_crud
from app.db.session import get_async_session
from app.schemas.link import LinkCreate
from app.schemas.survey_response import SurveyResponseRead

router = APIRouter()


@router.post("/link", response_model=dict[str, str])
async def create_survey_link(
    *,
    link_in: LinkCreate,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    """Create a link for a survey instance and return the URL and QR code."""
    survey_instance = await survey_instance_crud.get(db, id=link_in.survey_instance_id)

    if not survey_instance:
        raise HTTPException(
            status_code=404,
            detail="Survey instance not found",
        )

    # Create a link for the survey instance
    link = await link_crud.create(db, obj_in=link_in)

    # Generate URL
    url = f"/l/{link.id}"

    # Generate QR code
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(url, image_factory=factory)

    # Convert QR code to SVG string
    stream = io.BytesIO()
    img.save(stream)
    qr_svg = stream.getvalue().decode()

    return {"url": url, "qr_svg": qr_svg}


@router.get("/{id}/responses", response_model=list[SurveyResponseRead])
async def get_survey_instance_responses(
    *,
    id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
) -> list[SurveyResponseRead]:
    """Get all responses for a specific survey instance."""
    # Verify survey instance exists
    survey_instance = await survey_instance_crud.get(db, id=id)
    if not survey_instance:
        raise HTTPException(
            status_code=404,
            detail="Survey instance not found",
        )

    # Get responses for the survey instance
    responses = await survey_response_crud.get_by_survey_instance_id(db, survey_instance_id=id)

    # Explicitly load related entities and prepare the data for validation
    result = []
    for response in responses:
        # Eagerly load the answers relationship
        await db.refresh(response, ["answers"])

        # Get the survey instance to access org_id
        survey_instance = await survey_instance_crud.get(db, id=response.survey_instance_id)

        # Create a dict with the required fields for SurveyResponseRead
        response_data = {
            "id": response.id,
            "org_id": survey_instance.org_id,
            "survey_instance_id": response.survey_instance_id,
            "submitted_at": response.finished_at
            or response.started_at,  # Use finished_at if available, else started_at
            "email_hash": None,  # Default value
            "answers": {answer.question_text: answer.answer for answer in response.answers},
            "score": None,  # Default value
        }

        # Validate the response data
        result.append(SurveyResponseRead.model_validate(response_data))

    return result
