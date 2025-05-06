import csv
import io
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.event import event_crud
from app.crud.survey import survey_crud
from app.crud.survey_instance import survey_instance_crud
from app.crud.survey_response import survey_response_crud
from app.db.session import get_async_session

router = APIRouter()


@router.get("/events/{id}/stats")
async def get_event_stats(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Get completion percentage and average score for an event's surveys."""
    # Convert integer id to UUID by first converting to string
    try:
        event_uuid = uuid.UUID(str(id))
        event = await event_crud.get(db, id=event_uuid)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format",
        ) from err

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    # Get all survey instances for this event
    survey_instances = await survey_instance_crud.get_by_event_id(db, event_id=event_uuid)

    total_responses = 0
    total_score = 0
    total_possible_responses = 0

    for instance in survey_instances:
        # Get responses for this instance
        responses = await survey_response_crud.get_by_survey_instance_id(db, survey_instance_id=instance.id)

        total_responses += len(responses)

        # Calculate average score if there's a scoring mechanism
        # This is a placeholder - implement according to your scoring logic
        for response in responses:
            if "score" in response.answers:
                total_score += response.answers["score"]

        # Assuming we have a target response count per instance
        # This is a placeholder - adjust based on your business logic
        total_possible_responses += instance.target_response_count or 100

    completion_percentage = (total_responses / total_possible_responses * 100) if total_possible_responses > 0 else 0
    average_score = (total_score / total_responses) if total_responses > 0 else 0

    return {
        "completion_percentage": completion_percentage,
        "average_score": average_score,
        "total_responses": total_responses,
    }


@router.get("/surveys/{id}/responses/export")
async def export_survey_responses(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> StreamingResponse:
    """Export all responses for a survey as a CSV file."""
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

    # Get all instances of this survey
    survey_instances = await survey_instance_crud.get_by_survey_id(db, survey_id=survey_uuid)

    # Prepare CSV file
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header row - adjust based on your survey structure
    header = ["Response ID", "Survey Instance", "Event", "Timestamp", "Email"]

    # Add question headers based on survey schema
    questions = survey.schema.get("questions", [])
    for question in questions:
        header.append(question.get("label", question.get("id", "Unknown")))

    writer.writerow(header)

    # Write data rows
    for instance in survey_instances:
        responses = await survey_response_crud.get_by_survey_instance_id(db, survey_instance_id=instance.id)

        for response in responses:
            row = [
                response.id,
                instance.id,
                instance.event.name,
                response.created_at.isoformat(),
                response.email or "Anonymous",
            ]

            # Add answer data
            for question in questions:
                question_id = question.get("id")
                answer = response.answers.get(question_id, "")
                row.append(str(answer))

            writer.writerow(row)

    # Create response
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
    )
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{id}_responses.csv"

    return response
