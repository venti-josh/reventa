from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.survey import survey_crud
from app.crud.survey_answer import survey_answer_crud
from app.crud.survey_instance import survey_instance_crud
from app.crud.survey_response import survey_response_crud
from app.db.session import get_async_session
from app.schemas.survey_flow import (
    AnswerIn,
    NextQuestionOut,
    QuestionResponse,
    SurveyStartOut,
)
from app.services.followup_service import get_followup_question

router = APIRouter()


@router.post("/instance/{survey_instance_id}/start", response_model=SurveyStartOut)
async def start_survey(
    survey_instance_id: UUID = Path(...),
    db: AsyncSession = Depends(get_async_session),
) -> SurveyStartOut:
    """
    Start a new survey flow using only the survey instance ID.

    Creates a SurveyResponse record, sets up the first question,
    and returns the initial question to the client.
    """
    # Get the survey instance
    survey_instance = await survey_instance_crud.get(db, id=survey_instance_id)
    if not survey_instance:
        raise HTTPException(status_code=404, detail="Survey instance not found")

    # Get the associated survey
    survey_id = survey_instance.survey_id
    survey = await survey_crud.get(db, id=survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    if not isinstance(survey.schema, dict) or "questions" not in survey.schema:
        raise HTTPException(status_code=400, detail="Invalid survey schema")

    questions = survey.schema["questions"]
    if not isinstance(questions, list) or not questions:
        raise HTTPException(status_code=400, detail="Invalid survey questions")

    # Create a new survey response
    response_data = {
        "survey_id": survey_id,
        "survey_instance_id": survey_instance_id,
    }
    survey_response = await survey_response_crud.create(db, obj_in=response_data)

    # Get the first question from the survey
    first_question = questions[0]

    # Create an empty answer entry for tracking
    await survey_answer_crud.create(
        db,
        obj_in={
            "response_id": survey_response.id,
            "question_idx": 0,
            "question_text": first_question.get("text", ""),
            "is_followup": False,
        },
    )

    # Return the response ID and first question
    return SurveyStartOut(
        response_id=survey_response.id,
        question=QuestionResponse(
            text=first_question.get("text", ""),
            type=first_question.get("type", "text"),
            choices=first_question.get("choices"),
        ),
    )


@router.post("/responses/{response_id}/answer", response_model=NextQuestionOut)
# ruff: noqa: PLR0912, PLR0915
async def submit_answer(
    answer_in: AnswerIn,
    response_id: UUID = Path(...),
    db: AsyncSession = Depends(get_async_session),
) -> NextQuestionOut:
    """
    Submit an answer for the current question and get the next question.

    This endpoint:
    1. Stores or updates the answer for the current question
    2. Determines if a follow-up question is needed
    3. If yes, returns the follow-up question
    4. If no, advances to the next base question
    5. Returns "done=True" when all questions are answered
    """
    # Verify the survey response exists
    survey_response = await survey_response_crud.get(db, id=response_id)
    if not survey_response:
        raise HTTPException(status_code=404, detail="Survey response not found")

    # Check if the survey is already completed
    if survey_response.finished_at:
        raise HTTPException(status_code=400, detail="Survey already completed")

    # Get the survey to access the schema
    survey = await survey_crud.get(db, id=survey_response.survey_id)
    if not survey or not isinstance(survey.schema, dict) or "questions" not in survey.schema:
        raise HTTPException(status_code=400, detail="Invalid survey")

    questions = survey.schema["questions"]
    if not isinstance(questions, list) or not questions:
        raise HTTPException(status_code=400, detail="Invalid survey questions")

    # Get current question index and validate
    current_idx = survey_response.current_index
    if current_idx >= len(questions):
        # Survey is complete
        await survey_response_crud.mark_finished(db, response_id=response_id)
        return NextQuestionOut(done=True)

    # Get the current question
    current_base_question = questions[current_idx]
    current_question_text = current_base_question.get("text", "")
    current_question_description = current_base_question.get("description", "")

    # Get the answer entry
    answer_entry = await survey_answer_crud.get_by_response_and_question(
        db, response_id=response_id, question_idx=current_idx, is_followup=False
    )

    # If answer doesn't exist (should not happen) or it's a follow-up answer,
    # we need to check if we're currently handling a base question or follow-up
    is_answering_followup = False

    # Check if there's a follow-up for this question and if it exists in the database
    follow_up_entry = await survey_answer_crud.get_by_response_and_question(
        db, response_id=response_id, question_idx=current_idx, is_followup=True
    )

    # Determine if we're answering a follow-up question
    if follow_up_entry and not follow_up_entry.answer:
        # We're answering a follow-up that exists but hasn't been answered yet
        is_answering_followup = True
        answer_entry = follow_up_entry

    # Update or create the answer
    answer_value = None if answer_in.skipped else answer_in.answer

    if answer_entry:
        # Update existing answer
        await survey_answer_crud.update(
            db,
            db_obj=answer_entry,
            obj_in={"answer": answer_value},
        )

        # If this was a follow-up question, mark it as answered
        if is_answering_followup:
            # Make sure we're handling a follow-up question
            debug_msg = f"Processing follow-up answer: {answer_value} for question idx: {current_idx}"
            print(debug_msg)  # This helps with debugging
    else:
        # This shouldn't happen with the current flow but handle it just in case
        await survey_answer_crud.create(
            db,
            obj_in={
                "response_id": response_id,
                "question_idx": current_idx,
                "question_text": current_question_text,
                "is_followup": is_answering_followup,
                "answer": answer_value,
            },
        )

    # If we just answered a follow-up or skipped, move to next base question
    if is_answering_followup or answer_in.skipped:
        # Move to the next question
        survey_response = await survey_response_crud.increment_current_index(db, response_id=response_id)
        current_idx = survey_response.current_index

        # Check if we've reached the end of the survey
        if current_idx >= len(questions):
            await survey_response_crud.mark_finished(db, response_id=response_id)
            return NextQuestionOut(done=True)

        # Get the next base question
        next_question = questions[current_idx]

        # Create an empty answer entry for the next question
        await survey_answer_crud.create(
            db,
            obj_in={
                "response_id": response_id,
                "question_idx": current_idx,
                "question_text": next_question.get("text", ""),
                "is_followup": False,
            },
        )

        return NextQuestionOut(
            question=QuestionResponse(
                text=next_question.get("text", ""),
                type=next_question.get("type", "text"),
                choices=next_question.get("choices"),
            )
        )

    # If not skipped and not a follow-up, check if we need a follow-up question
    survey_description = survey.title

    # Check if this question allows follow-ups
    can_followup = current_base_question.get("can_followup", True)

    # Only generate follow-up if the question allows it
    follow_up = None
    if can_followup:
        follow_up = await get_followup_question(
            survey_description=survey_description,
            question_text=current_question_text,
            participant_answer=answer_value,
            question_description=current_question_description,
        )

    if follow_up:
        # Check if a follow-up question entry already exists
        existing_followup = await survey_answer_crud.get_by_response_and_question(
            db, response_id=response_id, question_idx=current_idx, is_followup=True
        )

        if existing_followup:
            # Update the existing follow-up instead of creating a new one
            await survey_answer_crud.update(
                db,
                db_obj=existing_followup,
                obj_in={"question_text": follow_up},
            )
        else:
            # Create a new follow-up question entry
            await survey_answer_crud.create(
                db,
                obj_in={
                    "response_id": response_id,
                    "question_idx": current_idx,
                    "question_text": follow_up,
                    "is_followup": True,
                },
            )

        # Return the follow-up question
        return NextQuestionOut(
            question=QuestionResponse(
                text=follow_up,
                type="text",  # Follow-ups are always free text
                choices=None,
            )
        )
    else:
        # No follow-up needed, move to the next question
        survey_response = await survey_response_crud.increment_current_index(db, response_id=response_id)
        current_idx = survey_response.current_index

        # Check if we've reached the end of the survey
        if current_idx >= len(questions):
            await survey_response_crud.mark_finished(db, response_id=response_id)
            return NextQuestionOut(done=True)

        # Get the next base question
        next_question = questions[current_idx]

        # Create an empty answer entry for the next question
        await survey_answer_crud.create(
            db,
            obj_in={
                "response_id": response_id,
                "question_idx": current_idx,
                "question_text": next_question.get("text", ""),
                "is_followup": False,
            },
        )

        return NextQuestionOut(
            question=QuestionResponse(
                text=next_question.get("text", ""),
                type=next_question.get("type", "text"),
                choices=next_question.get("choices"),
            )
        )
