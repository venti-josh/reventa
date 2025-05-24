import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


# Base models
class Question(BaseModel):
    """Base schema for survey question"""

    text: str
    type: str
    choices: list[str] | None = None
    description: str = ""
    can_followup: bool = True


class QuestionResponse(BaseModel):
    """Schema for question sent to frontend in API responses"""

    text: str
    type: str
    choices: list[str] | None = None


# SurveyResponse schemas
class SurveyResponseBase(BaseModel):
    """Base schema for survey response"""

    survey_id: uuid.UUID
    meta: dict[str, Any] | None = None


class SurveyResponseCreate(SurveyResponseBase):
    """Schema for creating survey response"""

    pass


class SurveyResponseUpdate(BaseModel):
    """Schema for updating survey response"""

    current_index: int | None = None
    finished_at: datetime | None = None


class SurveyResponseRead(SurveyResponseBase):
    """Schema for reading survey response"""

    id: uuid.UUID
    started_at: datetime
    finished_at: datetime | None = None
    current_index: int

    class Config:
        from_attributes = True


# SurveyAnswer schemas
class AnswerBase(BaseModel):
    """Base schema for survey answer"""

    response_id: uuid.UUID
    question_idx: int
    question_text: str
    is_followup: bool = False
    answer: dict[str, Any] | None = None


class AnswerCreate(AnswerBase):
    """Schema for creating survey answer"""

    pass


class AnswerUpdate(BaseModel):
    """Schema for updating survey answer"""

    answer: dict[str, Any] | None = None


class AnswerRead(AnswerBase):
    """Schema for reading survey answer"""

    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# API request/response schemas
class SurveyStartOut(BaseModel):
    """Response schema for starting a survey"""

    response_id: uuid.UUID
    question: QuestionResponse


class AnswerIn(BaseModel):
    """Request schema for submitting an answer"""

    answer: dict[str, Any] | None = None
    skipped: bool = False


class NextQuestionOut(BaseModel):
    """Response schema for the next question"""

    done: bool = False
    question: QuestionResponse | None = None
